"""Chat engine — LangChain chain with system prompt, memory, RAG context, and tools."""

from __future__ import annotations

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.prompt import SYSTEM_PROMPT
from app.rag import retrieve
from app.tools import check_availability

_store: dict[str, InMemoryChatMessageHistory] = {}


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def _build_chain():
    if not GROQ_API_KEY:
        return None

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0.3,
    )

    llm_with_tools = llm.bind_tools([check_availability])

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{context}\n\nUser: {input}"),
    ])

    chain = prompt | llm_with_tools

    return RunnableWithMessageHistory(
        chain,
        _get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


_chain = None


def _get_chain():
    global _chain
    if _chain is None:
        _chain = _build_chain()
    return _chain


def ask(user_msg: str, session_id: str = "default") -> str:
    """Process a user message and return the bot reply."""
    chain = _get_chain()
    if chain is None:
        return "Error: GROQ_API_KEY is not configured. Set it in .env or Vercel environment variables."

    context = retrieve(user_msg)
    context_block = f"Context from knowledge base:\n{context}" if context else ""

    config = {"configurable": {"session_id": session_id}}

    try:
        response = chain.invoke(
            {"input": user_msg, "context": context_block},
            config=config,
        )

        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_results = []
            for tc in response.tool_calls:
                if tc["name"] == "check_availability":
                    result = check_availability.invoke(tc["args"])
                    tool_results.append(result)

            if tool_results:
                history = _get_session_history(session_id)
                history.add_message(response)

                tool_context = "\n".join(
                    f"Tool result: {r}" for r in tool_results
                )
                followup = chain.invoke(
                    {
                        "input": f"Based on the tool results below, provide a helpful response to the user.\n\n{tool_context}\n\nOriginal question: {user_msg}",
                        "context": context_block,
                    },
                    config=config,
                )
                return followup.content if hasattr(followup, "content") else str(followup)

        return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        return f"I encountered an error: {e}"
