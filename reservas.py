"""Gestión de reservas, estados y manejo avanzado de excepciones."""
from datetime import datetime, timezone
from enum import Enum
from entidades import Entidad
from clientes import Cliente
from servicios import Servicio, decimal_positivo
from excepciones import DatosInvalidosError, ReservaInvalidaError, TransicionEstadoError
from logger_config import LOGGER


class EstadoReserva(str, Enum):
    """Estados permitidos para el ciclo de vida de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"


class Reserva(Entidad):
    """Relaciona un cliente con un servicio, duración, costo y estado."""

    def __init__(self, cliente, servicio, duracion_horas):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Cliente inválido.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Servicio inválido.")
        servicio.validar_disponibilidad()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = decimal_positivo(duracion_horas, "Duración")
        self.estado = EstadoReserva.PENDIENTE
        self.creada_en = datetime.now(timezone.utc)
        self.total = servicio.calcular_costo(self.duracion_horas)
        LOGGER.info("Reserva creada: %s", self.id)

    def confirmar(self):
        """Confirma únicamente reservas que todavía están pendientes."""
        if self.estado is not EstadoReserva.PENDIENTE:
            raise TransicionEstadoError("Solo se confirma una reserva pendiente.")
        self.estado = EstadoReserva.CONFIRMADA
        LOGGER.info("Reserva confirmada: %s", self.id)

    def cancelar(self, motivo="Sin especificar"):
        """Cancela una reserva activa y registra el motivo."""
        if self.estado is EstadoReserva.CANCELADA:
            raise TransicionEstadoError("La reserva ya está cancelada.")
        if not isinstance(motivo, str) or not motivo.strip():
            raise DatosInvalidosError("Motivo de cancelación obligatorio.")
        self.estado = EstadoReserva.CANCELADA
        LOGGER.warning("Reserva cancelada: %s | %s", self.id, motivo.strip())

    def procesar(self):
        """Procesa el costo y conserva la causa original si falla el cálculo."""
        if self.estado is EstadoReserva.CANCELADA:
            raise ReservaInvalidaError("No se procesa una reserva cancelada.")
        self.servicio.validar_disponibilidad()
        try:
            total = self.servicio.calcular_costo(self.duracion_horas)
        except DatosInvalidosError as exc:
            raise ReservaInvalidaError("No se pudo calcular el costo.") from exc
        else:
            LOGGER.info("Reserva procesada: %s | total=%s", self.id, total)
            return total
        finally:
            LOGGER.info("Fin del procesamiento de reserva %s", self.id)

    def resumen(self):
        """Resume el identificador, cliente, servicio, estado y costo."""
        return f"{self.id[:8]} | {self.cliente.nombre} | {self.servicio.nombre} | {self.estado.value} | ${self.total}"


class GestorReservas:
    """Administra la creación, consulta y cancelación de reservas."""

    def __init__(self):
        self._reservas = []

    @property
    def reservas(self):
        """Devuelve una vista inmutable de las reservas creadas."""
        return tuple(self._reservas)

    def crear(self, cliente, servicio, duracion_horas):
        """Crea una reserva y la agrega al listado solo si es válida."""
        reserva = Reserva(cliente, servicio, duracion_horas)
        self._reservas.append(reserva)
        return reserva

    def buscar(self, identificador):
        """Busca una reserva por ID y registra el fallo si no existe."""
        for reserva in self._reservas:
            if reserva.id == identificador:
                return reserva
        LOGGER.error("Búsqueda de reserva fallida; ID inexistente: %s", identificador)
        raise LookupError(f"Reserva inexistente: {identificador}")

    def cancelar(self, identificador, motivo="Sin especificar"):
        """Localiza una reserva y solicita su cancelación."""
        self.buscar(identificador).cancelar(motivo)
