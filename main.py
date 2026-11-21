"""Punto de entrada de Software FJ."""
from clientes import Cliente, GestorClientes
from servicios import CatalogoServicios, ServicioSala, ServicioEquipo, ServicioAsesoria
from reservas import GestorReservas
from excepciones import ErrorSistemaFJ
from logger_config import LOGGER

def demostrar_sistema():
    clientes, catalogo, reservas = GestorClientes(), CatalogoServicios(), GestorReservas()
    print("=" * 65)
    print("SOFTWARE FJ | GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 65)

    try:
        cliente = clientes.registrar(Cliente("María Gómez", "maria@example.com", "3105551234"))
        print("\nCliente:", cliente.resumen())
    except ErrorSistemaFJ as exc:
        print("Error controlado al registrar cliente:", exc)
        LOGGER.exception("Registro inicial fallido")

    servicios = [
        ServicioSala("Sala Norte", 75000, 10),
        ServicioEquipo("Proyector", 35000, 4),
        ServicioAsesoria("Asesoría Python", 95000, "Programación orientada a objetos"),
    ]
    for servicio in servicios:
        try:
            catalogo.agregar(servicio)
            print("\nServicio:", servicio.resumen())
        except ErrorSistemaFJ as exc:
            print("Error controlado de servicio:", exc)
            LOGGER.exception("Registro de servicio fallido")

    try:
        reserva = reservas.crear(cliente, servicios[0], 2)
        reserva.confirmar()
        print("\nReserva:", reserva.resumen())
        print("Total procesado:", reserva.procesar())
    except ErrorSistemaFJ as exc:
        print("Error controlado de reserva:", exc)
        LOGGER.exception("Demostración de reserva fallida")
    finally:
        print("Finalizó el bloque de demostración de reservas.")

    try:
        costo = servicios[1].calcular_costo(2, impuesto=0.19)
    except ErrorSistemaFJ as exc:
        print("No fue posible calcular el costo:", exc)
        LOGGER.exception("Cálculo demostrativo fallido")
    else:
        print("\nCosto de dos equipos con impuesto:", costo)

    print("\nEjecución finalizada. Revise logs/sistema.log.")

if __name__ == "__main__":
    demostrar_sistema()
