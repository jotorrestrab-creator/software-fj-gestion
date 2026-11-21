"""Excepciones específicas del sistema Software FJ."""
from logger_config import LOGGER


class ErrorSistemaFJ(Exception):
    """Clase base: registra automáticamente cada error de dominio detectado."""

    def __init__(self, mensaje):
        LOGGER.error("%s: %s", type(self).__name__, mensaje)
        super().__init__(mensaje)


class DatosInvalidosError(ErrorSistemaFJ, ValueError):
    """Se genera cuando un dato no cumple las reglas de validación."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se genera cuando se intenta utilizar un servicio no disponible."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se genera cuando una reserva no puede procesarse."""


class TransicionEstadoError(ErrorSistemaFJ):
    """Se genera cuando se solicita un cambio de estado no permitido."""
