"""Gestión de reservas con estados y excepciones."""
from datetime import datetime, timezone
from enum import Enum
from entidades import Entidad
from clientes import Cliente
from servicios import Servicio, decimal_positivo
from excepciones import DatosInvalidosError, ReservaInvalidaError, TransicionEstadoError
from logger_config import LOGGER

class EstadoReserva(str, Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"

class Reserva(Entidad):
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
        if self.estado is not EstadoReserva.PENDIENTE:
            raise TransicionEstadoError("Solo se confirma una reserva pendiente.")
        self.estado = EstadoReserva.CONFIRMADA
        LOGGER.info("Reserva confirmada: %s", self.id)

    def cancelar(self, motivo="Sin especificar"):
        if self.estado is EstadoReserva.CANCELADA:
            raise TransicionEstadoError("La reserva ya está cancelada.")
        if not isinstance(motivo, str) or not motivo.strip():
            raise DatosInvalidosError("Motivo de cancelación obligatorio.")
        self.estado = EstadoReserva.CANCELADA
        LOGGER.warning("Reserva cancelada: %s | %s", self.id, motivo.strip())

    def procesar(self):
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
        return f"{self.id[:8]} | {self.cliente.nombre} | {self.servicio.nombre} | {self.estado.value} | ${self.total}"

class GestorReservas:
    def __init__(self):
        self._reservas = []

    @property
    def reservas(self):
        return tuple(self._reservas)

    def crear(self, cliente, servicio, duracion_horas):
        reserva = Reserva(cliente, servicio, duracion_horas)
        self._reservas.append(reserva)
        return reserva

    def buscar(self, identificador):
        for reserva in self._reservas:
            if reserva.id == identificador:
                return reserva
        raise LookupError(f"Reserva inexistente: {identificador}")

    def cancelar(self, identificador, motivo="Sin especificar"):
        self.buscar(identificador).cancelar(motivo)
"