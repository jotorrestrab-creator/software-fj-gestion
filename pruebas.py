"""Batería reproducible de 15 escenarios de prueba."""
from clientes import Cliente, GestorClientes
from servicios import CatalogoServicios, ServicioSala, ServicioEquipo, ServicioAsesoria
from reservas import GestorReservas
from logger_config import LOGGER

def ejecutar_pruebas():
    clientes, catalogo, reservas = GestorClientes(), CatalogoServicios(), GestorReservas()
    correctos = fallidos = 0

    def ejecutar(n, titulo, accion, error_esperado=False):
        nonlocal correctos, fallidos
        try:
            resultado = accion()
        except Exception as exc:
            if error_esperado:
                correctos += 1
                print(f"[{n:02}] OK: {titulo} -> {type(exc).__name__}: {exc}")
                LOGGER.info("Prueba %s correcta; excepción esperada: %s", n, type(exc).__name__)
            else:
                fallidos += 1
                print(f"[{n:02}] FALLÓ: {titulo} -> {type(exc).__name__}: {exc}")
                LOGGER.exception("Prueba %s fallida: %s", n, titulo)
        else:
            if error_esperado:
                fallidos += 1
                print(f"[{n:02}] FALLÓ: {titulo}; se esperaba excepción.")
            else:
                correctos += 1
                detalle = resultado.resumen() if hasattr(resultado, "resumen") else str(resultado)
                print(f"[{n:02}] OK: {titulo} -> {detalle}")
                LOGGER.info("Prueba %s correcta: %s", n, titulo)

    cliente = Cliente("Ana Torres", "ana@example.com", "3001234567")
    ejecutar(1, "Registrar cliente válido", lambda: clientes.registrar(cliente))
    ejecutar(2, "Rechazar correo inválido", lambda: Cliente("Luis Pérez", "correo", "3001234568"), True)
    ejecutar(3, "Rechazar cliente duplicado", lambda: clientes.registrar(Cliente("Ana Otra", "ana@example.com", "3001234569")), True)

    sala = ServicioSala("Sala Ejecutiva", 80000, 12)
    equipo = ServicioEquipo("Video beam", 45000, 5)
    asesoria = ServicioAsesoria("Asesoría Python", 100000, "Desarrollo de software")
    ejecutar(4, "Crear servicio de sala", lambda: catalogo.agregar(sala))
    ejecutar(5, "Crear servicio de equipo", lambda: catalogo.agregar(equipo))
    ejecutar(6, "Crear servicio de asesoría", lambda: catalogo.agregar(asesoria))
    ejecutar(7, "Rechazar sala con capacidad cero", lambda: ServicioSala("Sala errónea", 40000, 0), True)
    ejecutar(8, "Calcular costo con impuesto y descuento", lambda: sala.calcular_costo(2, impuesto=0.19, descuento=0.10))

    reserva = reservas.crear(cliente, sala, 2)
    ejecutar(9, "Crear reserva válida", lambda: reserva)
    ejecutar(10, "Confirmar reserva", lambda: (reserva.confirmar(), reserva)[1])
    ejecutar(11, "Procesar reserva confirmada", lambda: reserva.procesar())

    equipo.cambiar_disponibilidad(False)
    ejecutar(12, "Rechazar reserva de servicio no disponible", lambda: reservas.crear(cliente, equipo, 1), True)
    ejecutar(13, "Rechazar duración cero", lambda: reservas.crear(cliente, asesoria, 0), True)
    ejecutar(14, "Cancelar reserva confirmada", lambda: (reserva.cancelar("Solicitud del cliente"), reserva)[1])
    ejecutar(15, "Rechazar procesamiento de reserva cancelada", lambda: reserva.procesar(), True)

    print(f"\nResumen: {correctos} correctas; {fallidos} fallidas; total {correctos + fallidos}.")
    LOGGER.info("Resumen de pruebas: %s correctas, %s fallidas", correctos, fallidos)
    return correctos, fallidos

if __name__ == "__main__":
    ejecutar_pruebas()
