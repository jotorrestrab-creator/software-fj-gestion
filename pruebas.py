"""Pruebas funcionales y de manejo de excepciones de Software FJ."""
from clientes import Cliente, GestorClientes
from servicios import (
    CatalogoServicios, ServicioSala, ServicioEquipo, ServicioAsesoria
)
from reservas import GestorReservas
from excepciones import DatosInvalidosError, ReservaInvalidaError, TransicionEstadoError
from logger_config import LOGGER\nfrom pathlib import Path


def ejecutar_pruebas():
    """Ejecuta casos positivos y negativos sin detenerse ante errores esperados."""
    clientes = GestorClientes()
    catalogo = CatalogoServicios()
    reservas = GestorReservas()
    correctos = fallidos = 0

    def ejecutar(numero, titulo, accion, error_esperado=False):
        """Aísla cada caso, informa su resultado y permite continuar la batería."""
        nonlocal correctos, fallidos
        try:
            resultado = accion()
        except Exception as exc:
            if error_esperado:
                correctos += 1
                print(f"[{numero:02}] OK: {titulo} -> {type(exc).__name__}: {exc}")
                LOGGER.info("Caso %s: excepción esperada (%s): %s",
                            numero, type(exc).__name__, titulo)
            else:
                fallidos += 1
                print(f"[{numero:02}] FALLÓ: {titulo} -> {type(exc).__name__}: {exc}")
                LOGGER.exception("Caso %s fallido: %s", numero, titulo)
        else:
            if error_esperado:
                fallidos += 1
                print(f"[{numero:02}] FALLÓ: {titulo}; se esperaba una excepción.")
                LOGGER.error("Caso %s: no se produjo la excepción esperada: %s",
                             numero, titulo)
            else:
                correctos += 1
                detalle = resultado.resumen() if hasattr(resultado, "resumen") else str(resultado)
                print(f"[{numero:02}] OK: {titulo} -> {detalle}")
                LOGGER.info("Caso %s correcto: %s", numero, titulo)

    # Datos de prueba iniciales.
    cliente = Cliente("Ana Torres", "ana@example.com", "3001234567")
    sala = ServicioSala("Sala Ejecutiva", 80000, 12)
    equipo = ServicioEquipo("Video beam", 45000, 5)
    asesoria = ServicioAsesoria("Asesoría Python", 100000, "Desarrollo de software")

    ejecutar(1, "Registrar cliente válido", lambda: clientes.registrar(cliente))
    ejecutar(2, "Rechazar correo inválido",
             lambda: Cliente("Luis Pérez", "correo", "3001234568"), True)
    ejecutar(3, "Rechazar cliente duplicado",
             lambda: clientes.registrar(Cliente("Ana Otra", "ana@example.com", "3001234569")), True)
    ejecutar(4, "Agregar servicio de sala", lambda: catalogo.agregar(sala))
    ejecutar(5, "Agregar servicio de equipo", lambda: catalogo.agregar(equipo))
    ejecutar(6, "Agregar servicio de asesoría", lambda: catalogo.agregar(asesoria))
    ejecutar(7, "Rechazar sala con capacidad cero",
             lambda: ServicioSala("Sala errónea", 40000, 0), True)
    ejecutar(8, "Calcular costo con impuesto y descuento",
             lambda: sala.calcular_costo(2, impuesto=0.19, descuento=0.10))
    ejecutar(9, "Crear reserva válida", lambda: reservas.crear(cliente, sala, 2))
    reserva = reservas.reservas[-1]
    ejecutar(10, "Confirmar reserva", lambda: (reserva.confirmar(), reserva)[1])
    ejecutar(11, "Procesar reserva confirmada", lambda: reserva.procesar())

    equipo.cambiar_disponibilidad(False)
    ejecutar(12, "Rechazar reserva de servicio no disponible",
             lambda: reservas.crear(cliente, equipo, 1), True)
    ejecutar(13, "Rechazar duración cero",
             lambda: reservas.crear(cliente, asesoria, 0), True)
    ejecutar(14, "Cancelar reserva confirmada",
             lambda: (reserva.cancelar("Solicitud del cliente"), reserva)[1])
    ejecutar(15, "Rechazar procesamiento de reserva cancelada",
             lambda: reserva.procesar(), True)

    ejecutar(16, "Rechazar tasa de impuesto negativa",
             lambda: sala.calcular_costo(1, impuesto=-0.01), True)
    ejecutar(17, "Rechazar descuento superior al 100 por ciento",
             lambda: sala.calcular_costo(1, descuento=1.01), True)
    ejecutar(18, "Rechazar objeto que no es un servicio",
             lambda: catalogo.agregar("servicio incorrecto"), True)
    ejecutar(19, "Rechazar confirmación de reserva cancelada",
             lambda: reserva.confirmar(), True)
    ejecutar(20, "Rechazar segunda cancelación",
             lambda: reserva.cancelar("Segundo intento"), True)
    ejecutar(21, "Rechazar cantidad de equipos superior al inventario",
             lambda: equipo.calcular_costo(6), True)
    ejecutar(22, "Rechazar duración no numérica",
             lambda: reservas.crear(cliente, sala, "dos horas"), True)
    ejecutar(23, "Informar búsqueda de servicio inexistente",
             lambda: catalogo.buscar("id-inexistente"), True)
    ejecutar(24, "Rechazar creación de reserva con cliente inválido",
             lambda: reservas.crear("no es cliente", sala, 1), True)
    ejecutar(25, "Rechazar cantidad fraccionaria de equipos",
             lambda: equipo.calcular_costo(1.5), True)
    ejecutar(26, "Rechazar cantidad de equipos no numérica",
             lambda: equipo.calcular_costo("varios"), True)

    def comprobar_encadenamiento():
        """Provoca un fallo interno y comprueba que se conserva como causa."""
        reserva_prueba = reservas.crear(cliente, sala, 1)

        def calculo_con_fallo(*args, **kwargs):
            raise DatosInvalidosError("Fallo interno simulado para probar el encadenamiento.")

        reserva_prueba.servicio.calcular_costo = calculo_con_fallo
        try:
            reserva_prueba.procesar()
        except ReservaInvalidaError as exc:
            if not isinstance(exc.__cause__, DatosInvalidosError):
                raise AssertionError("No se conservó la excepción original como causa.")
            return f"Causa original conservada: {type(exc.__cause__).__name__}"
        raise AssertionError("Se esperaba ReservaInvalidaError.")

    ejecutar(27, "Verificar encadenamiento de excepciones",
             comprobar_encadenamiento)

    def comprobar_registro_error():
        """Genera un error único y verifica su escritura efectiva en el archivo."""
        identificador = "PRUEBA_LOG_FASE4_2026"
        try:
            raise DatosInvalidosError(identificador)
        except DatosInvalidosError:
            pass
        archivo_log = Path(__file__).resolve().parent / "logs" / "sistema.log"
        contenido_log = archivo_log.read_text(encoding="utf-8")
        if identificador not in contenido_log:
            raise AssertionError("El error no aparece en logs/sistema.log.")
        return f"Error registrado en {archivo_log.relative_to(Path(__file__).resolve().parent)}"

    ejecutar(28, "Verificar escritura efectiva de errores en el log",
             comprobar_registro_error)

    total = correctos + fallidos
    print(f"\nResumen: {correctos} correctas; {fallidos} fallidas; total {total}.")
    LOGGER.info("Resumen de pruebas: %s correctas, %s fallidas", correctos, fallidos)
    return correctos, fallidos


if __name__ == "__main__":
    ejecutar_pruebas()
