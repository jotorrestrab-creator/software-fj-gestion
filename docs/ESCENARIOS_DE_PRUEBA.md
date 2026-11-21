# Escenarios de prueba — Software FJ

La batería automatizada de `pruebas.py` ejecuta 24 escenarios independientes. Los casos negativos se consideran satisfactorios cuando se genera una excepción y el programa continúa con el siguiente caso.

| N.º | Operación | Resultado esperado |
|---:|---|---|
| 1 | Registrar cliente válido | Registro correcto |
| 2 | Registrar correo inválido | Excepción de validación |
| 3 | Registrar correo duplicado | Excepción de validación |
| 4 | Agregar servicio de sala | Servicio agregado |
| 5 | Agregar servicio de equipo | Servicio agregado |
| 6 | Agregar servicio de asesoría | Servicio agregado |
| 7 | Crear sala con capacidad cero | Excepción de validación |
| 8 | Calcular costo con impuesto y descuento | Total calculado |
| 9 | Crear reserva válida | Reserva pendiente |
| 10 | Confirmar reserva | Estado confirmado |
| 11 | Procesar reserva confirmada | Total calculado y evento registrado |
| 12 | Reservar servicio no disponible | Excepción controlada |
| 13 | Crear reserva con duración cero | Excepción de validación |
| 14 | Cancelar reserva confirmada | Estado cancelado |
| 15 | Procesar reserva cancelada | Excepción controlada |
| 16 | Calcular con impuesto negativo | Excepción de validación |
| 17 | Calcular con descuento superior al 100 % | Excepción de validación |
| 18 | Agregar un objeto que no sea Servicio | Excepción de validación |
| 19 | Confirmar una reserva cancelada | Transición rechazada |
| 20 | Cancelar una reserva dos veces | Transición rechazada |
| 21 | Solicitar más equipos que el inventario | Excepción de validación |
| 22 | Crear reserva con duración no numérica | Excepción de validación |
| 23 | Buscar un servicio inexistente | Búsqueda fallida controlada |
| 24 | Crear reserva con cliente de tipo incorrecto | Excepción de validación |\n| 25 | Solicitar cantidad fraccionaria de equipos | Excepción de validación |\n| 26 | Solicitar cantidad de equipos no numérica | Excepción de validación |

## Ejecución y evidencia

Desde la carpeta raíz del repositorio, ejecutar:

```bash
python pruebas.py
python main.py
```

La salida de consola permite verificar los resultados. El archivo `logs/sistema.log` conserva eventos y errores detectados. Los registros de clientes, servicios y reservas permanecen en memoria; el archivo de log no almacena esos datos de negocio.
