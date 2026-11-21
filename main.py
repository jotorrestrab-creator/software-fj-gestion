"""Punto de entrada y demostración controlada de Software FJ."""
from clientes import Cliente, GestorClientes
from servicios import CatalogoServicios, ServicioSala, ServicioEquipo, ServicioAsesoria
from reservas import GestorReservas
from excepciones import ErrorSistemaFJ
from logger_config import LOGGER


def demostrar_sistema():
    """Ejecuta un recorrido demostrativo y aísla los errores por operación."""
    clientes = GestorClientes()
    catalogo = CatalogoServicios()
    reservas = GestorReservas()
    cliente = None
    servicios_creados = []

    print("=" * 65)
    print("SOFTWARE FJ | GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 65)

    try:
        cliente = clientes.registrar(
            Cliente("María Gómez", "maria@example.com", "3105551234")
        )
        print("\nCliente:", cliente.resumen())
    except ErrorSistemaFJ as exc:
        print("Error controlado al registrar cliente:", exc)
        LOGGER.exception("Registro inicial fallido")

    # Cada servicio se construye y agrega de forma independiente.
    definiciones = (
        lambda: ServicioSala("Sala Norte", 75000, 10),
        lambda: ServicioEquipo("Proyector", 35000, 4),
        lambda: ServicioAsesoria(
            "Asesoría Python", 95000, "Programación orientada a objetos"
        ),
    )
    for crear_servicio in definiciones:
        try:
            servicio = catalogo.agregar(crear_servicio())
            servicios_creados.append(servicio)
            print("\nServicio:", servicio.resumen())
        except ErrorSistemaFJ as exc:
            print("Error controlado de servicio:", exc)
            LOGGER.exception("Creación o registro de servicio fallido")

    try:
        if cliente is None:
            raise ErrorSistemaFJ("No existe un cliente válido para crear la reserva.")
        if not servicios_creados:
            raise ErrorSistemaFJ("No hay servicios disponibles para reservar.")
        reserva = reservas.crear(cliente, servicios_creados[0], 2)
        reserva.confirmar()
        print("\nReserva:", reserva.resumen())
        print("Total procesado:", reserva.procesar())
    except ErrorSistemaFJ as exc:
        print("Error controlado de reserva:", exc)
        LOGGER.exception("Demostración de reserva fallida")
    finally:
        print("Finalizó el bloque de demostración de reservas.")

    if len(servicios_creados) > 1:
        try:
            costo = servicios_creados[1].calcular_costo(2, impuesto=0.19)
        except ErrorSistemaFJ as exc:
            print("No fue posible calcular el costo:", exc)
            LOGGER.exception("Cálculo demostrativo fallido")
        else:
            print("\nCosto de dos equipos con impuesto:", costo)

    print("\nEjecución finalizada. Revise logs/sistema.log.")


if __name__ == "__main__":
    demostrar_sistema()
