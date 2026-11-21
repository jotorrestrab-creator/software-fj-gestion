# Escenarios de prueba — Software FJ

La batería de `pruebas.py` contempla 15 escenarios. Los casos negativos se consideran exitosos cuando el programa genera la excepción prevista y continúa con los demás escenarios.

| N.º | Operación | Resultado esperado |
|---:|---|---|
| 1 | Registrar cliente válido | Registro correcto |
| 2 | Registrar correo inválido | Excepción de validación |
| 3 | Registrar correo duplicado | Excepción de validación |
| 4 | Crear servicio de sala | Servicio agregado |
| 5 | Crear servicio de equipo | Servicio agregado |
| 6 | Crear servicio de asesoría | Servicio agregado |
| 7 | Crear sala con capacidad cero | Excepción de validación |
| 8 | Calcular costo con impuesto y descuento | Total calculado |
| 9 | Crear reserva válida | Reserva pendiente |
| 10 | Confirmar reserva | Estado confirmado |
| 11 | Procesar reserva confirmada | Total calculado y evento registrado |
| 12 | Reservar servicio no disponible | Excepción controlada |
| 13 | Crear reserva con duración cero | Excepción de validación |
| 14 | Cancelar reserva | Estado cancelado |
| 15 | Procesar reserva cancelada | Excepción controlada |

## Evidencia
Ejecutar `python pruebas.py` desde la carpeta raíz. Conservar la salida de consola y `logs/sistema.log` como evidencia de ejecución.
