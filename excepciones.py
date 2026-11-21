"""Excepciones específicas del sistema."""
class ErrorSistemaFJ(Exception):
    """Error base del dominio Software FJ."""
class DatosInvalidosError(ErrorSistemaFJ, ValueError):
    """Dato inválido."""
class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Servicio no disponible."""
class ReservaInvalidaError(ErrorSistemaFJ):
    """Reserva inválida."""
class TransicionEstadoError(ErrorSistemaFJ):
    """Transición de estado no permitida."""
