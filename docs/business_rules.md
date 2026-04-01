# Reglas de Negocio y Lógica de Agenda

## 1. Capacidad operativa ("La Cuota")

| Parámetro | Valor |
|-----------|-------|
| Días operativos | Lunes a jueves |
| Ventana quirúrgica | 09:00 a 13:00 |
| Capacidad diaria máxima | 240 minutos |
| Lógica de ocupación | Cada cita resta minutos de la capacidad total |

> Viernes, sábado y domingo bloqueados para cirugía por defecto.

## 2. Tabla de servicios y tiempos

### Gatos (sin límite de cantidad, solo de tiempo)

| Servicio | Tiempo (min) |
|----------|-------------|
| Esterilización gato macho | 12 |
| Esterilización gata hembra | 15 |

### Perros (sujeto a restricción de cantidad)

| Categoría | Tiempo (min) |
|-----------|-------------|
| Perro macho (cualquier peso) | 30 |
| Perra 0–10 kg | 45 |
| Perra 10–20 kg | 50 |
| Perra 20–30 kg | 60 |
| Perra 30–40 kg | 60 |
| Perra >40 kg | 70 |

## 3. Algoritmo de restricción y bloqueo ("El Tetris")

Para confirmar una fecha, **ambas** condiciones deben cumplirse:

### Regla 1: Validación de tiempo

```
(Minutos ya ocupados) + (Minutos de la nueva cita) ≤ 240
```

### Regla 2: Límite de perros (máximo 2)

```
Si la nueva cita es PERRO:
  (Número de perros del día) + 1 ≤ 2
```

- Si ya hay 2 perros en un día → se bloquea para nuevos perros aunque queden minutos.
- Esta regla **no** se aplica a gatos. Un día con 2 perros puede seguir aceptando gatos.

## 4. Ventanas de entrega por especie

| Especie | Ventana de entrega | Días aplicables |
|---------|--------------------|-----------------|
| Gatos | 08:00–09:00 (estricto) | Lunes a viernes |
| Perros | 09:00–10:30 (estricto) | Lunes a jueves (días operativos) |

### Reglas de validación

- **Gatos:** No se confirma ninguna cita fuera de 08:00–09:00.
- **Perros:** No se confirma ninguna cita fuera de 09:00–10:30.
- El cliente **nunca** elige hora concreta de quirófano; solo elige el **día**.

## 5. Protocolo de comunicación

| Regla | Descripción |
|-------|-------------|
| Ocultar horarios quirúrgicos | El cliente solo elige el DÍA, no la hora |
| Mensaje de entrega | Al confirmar, indicar la ventana correcta por especie |
| Protocolo de ayuno | Instrucciones de ayuno (desde medianoche) en la confirmación |

## 6. Restricciones adicionales

| Regla | Detalle |
|-------|---------|
| Celo en perras | **Rechazar**: esperar 2 meses tras fin del celo |
| Celo en gatos | **Aceptar**: los gatos pueden operarse en celo |
| Analítica preoperatoria | Obligatoria en animales >6 años |
| Más de 1 mascota | Derivar a llamada telefónica |
| Emergencias | Fuera de alcance, derivar a otro centro |
| Cancelación | Avisar con al menos 24h de antelación; si no, posible recargo |
| Microchip + rabia | Opcionales, se pueden hacer el día de la cirugía bajo anestesia |
