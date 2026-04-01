"""RAG pipeline — fetches the official pre-surgery URL, chunks it, and retrieves via BM25."""

from __future__ import annotations

import os
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from app.config import RAG_SOURCE_URL

_DATA_DIR = Path(__file__).parent / "data"
_CACHE_FILE = _DATA_DIR / "rag_source.txt"

_chunks: list[str] = []
_bm25: BM25Okapi | None = None


def _fetch_content() -> str:
    """Download the official source; fall back to the cached copy."""
    try:
        import requests
        from bs4 import BeautifulSoup

        resp = requests.get(RAG_SOURCE_URL, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        main = soup.find("main") or soup.find("article") or soup.body or soup
        text = main.get_text(separator="\n", strip=True)
        if len(text) > 200:
            _CACHE_FILE.write_text(text, encoding="utf-8")
            return text
    except Exception:
        pass
    if _CACHE_FILE.exists():
        return _CACHE_FILE.read_text(encoding="utf-8")
    return ""


def _split_text(text: str, chunk_size: int = 300, overlap: int = 80) -> list[str]:
    sentences = re.split(r"(?<=[.!?\n])\s+", text)
    chunks: list[str] = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) > chunk_size and current:
            chunks.append(current.strip())
            words = current.split()
            overlap_words = words[-max(1, overlap // 5) :]
            current = " ".join(overlap_words) + " " + sent
        else:
            current = current + " " + sent if current else sent
    if current.strip():
        chunks.append(current.strip())
    return chunks


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def init_rag() -> None:
    """Build the BM25 index from the RAG source. Call once at startup."""
    global _chunks, _bm25
    content = _fetch_content()
    if not content:
        return
    _chunks = _split_text(content)
    tokenized = [_tokenize(c) for c in _chunks]
    if tokenized:
        _bm25 = BM25Okapi(tokenized)


def retrieve(query: str, top_k: int = 3) -> str:
    """Return the top-k most relevant chunks for a query, joined as a string."""
    if not _bm25 or not _chunks:
        return ""
    tokens = _tokenize(query)
    scores = _bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    selected = [_chunks[i] for i in top_indices if scores[i] > 0]
    return "\n\n".join(selected)
