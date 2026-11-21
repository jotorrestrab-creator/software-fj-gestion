"""Clases abstractas y especializadas para administrar servicios."""
from abc import abstractmethod
from decimal import Decimal, InvalidOperation
from entidades import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError
from logger_config import LOGGER


def decimal_positivo(valor, campo):
    """Convierte un valor a Decimal y exige que sea finito y mayor que cero."""
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise DatosInvalidosError(f"{campo} debe ser numérico.") from exc
    if not numero.is_finite() or numero <= 0:
        raise DatosInvalidosError(f"{campo} debe ser mayor que cero.")
    return numero


def decimal_tasa(valor, campo):
    """Valida una tasa decimal comprendida entre cero y uno."""
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise DatosInvalidosError(f"{campo} debe ser numérico.") from exc
    if not numero.is_finite() or not Decimal("0") <= numero <= Decimal("1"):
        raise DatosInvalidosError(f"{campo} debe estar entre 0 y 1.")
    return numero


class Servicio(Entidad):
    """Define los atributos y operaciones comunes de cualquier servicio."""

    def __init__(self, nombre, tarifa_base):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        self.nombre = nombre.strip()
        self.tarifa_base = decimal_positivo(tarifa_base, "La tarifa")
        self._disponible = True

    @property
    def disponible(self):
        """Expone el estado de disponibilidad sin permitir asignación directa."""
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        """Actualiza la disponibilidad y registra el cambio."""
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser booleana.")
        self._disponible = disponible
        LOGGER.info("Disponibilidad de %s: %s", self.nombre, disponible)

    def validar_disponibilidad(self):
        """Impide reservar servicios marcados como no disponibles."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Servicio no disponible: {self.nombre}")

    def calcular_costo(self, cantidad=1, *, impuesto=0, descuento=0):
        """Calcula el costo base; impuesto y descuento son tasas opcionales."""
        unidades = decimal_positivo(cantidad, "La cantidad")
        tasa = decimal_tasa(impuesto, "El impuesto")
        rebaja = decimal_tasa(descuento, "El descuento")
        total = self.tarifa_base * unidades * (Decimal("1") - rebaja) * (Decimal("1") + tasa)
        return total.quantize(Decimal("0.01"))

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible del servicio concreto."""

    @abstractmethod
    def validar_parametros(self, **parametros):
        """Valida los parámetros particulares de cada tipo de servicio."""

    def resumen(self):
        """Entrega un resumen común para mostrar el servicio."""
        return f"{self.describir()} | tarifa ${self.tarifa_base}"


class ServicioSala(Servicio):
    """Servicio de alquiler de salas con capacidad máxima de asistentes."""

    def __init__(self, nombre, tarifa_base, capacidad):
        super().__init__(nombre, tarifa_base)
        self.capacidad = capacidad
        self.validar_parametros(capacidad=capacidad)

    def describir(self):
        return f"Sala {self.nombre}, capacidad {self.capacidad}"

    def validar_parametros(self, **parametros):
        capacidad = parametros.get("capacidad", getattr(self, "capacidad", None))
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("Capacidad debe ser entero positivo.")

    def calcular_costo(self, cantidad=1, *, impuesto=0, descuento=0):
        """Calcula el alquiler de sala por unidad de tiempo solicitada."""
        self.validar_parametros(capacidad=self.capacidad)
        return super().calcular_costo(cantidad, impuesto=impuesto, descuento=descuento)


class ServicioEquipo(Servicio):
    """Servicio de alquiler de equipos con inventario limitado."""

    def __init__(self, nombre, tarifa_base, unidades_disponibles):
        super().__init__(nombre, tarifa_base)
        self.unidades_disponibles = unidades_disponibles
        self.validar_parametros(unidades_disponibles=unidades_disponibles)

    def describir(self):
        return f"Equipo {self.nombre}, unidades {self.unidades_disponibles}"

    def validar_parametros(self, **parametros):
        unidades = parametros.get("unidades_disponibles", getattr(self, "unidades_disponibles", None))
        if not isinstance(unidades, int) or isinstance(unidades, bool) or unidades < 0:
            raise DatosInvalidosError("Unidades disponibles deben ser entero no negativo.")

    def calcular_costo(self, cantidad=1, *, impuesto=0, descuento=0):
        """Calcula el alquiler del equipo y verifica que exista inventario."""
        self.validar_parametros(unidades_disponibles=self.unidades_disponibles)
        if Decimal(str(cantidad)) > self.unidades_disponibles:
            raise DatosInvalidosError("La cantidad solicitada supera las unidades disponibles.")
        return super().calcular_costo(cantidad, impuesto=impuesto, descuento=descuento)


class ServicioAsesoria(Servicio):
    """Servicio de asesoría profesional por horas contratadas."""

    def __init__(self, nombre, tarifa_base, especialidad):
        super().__init__(nombre, tarifa_base)
        self.especialidad = especialidad
        self.validar_parametros(especialidad=especialidad)

    def describir(self):
        return f"Asesoría {self.nombre}, especialidad {self.especialidad}"

    def validar_parametros(self, **parametros):
        especialidad = parametros.get("especialidad", getattr(self, "especialidad", None))
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            raise DatosInvalidosError("Especialidad debe tener al menos 3 caracteres.")

    def calcular_costo(self, cantidad=1, *, impuesto=0, descuento=0):
        """Calcula el valor de la asesoría según las horas contratadas."""
        self.validar_parametros(especialidad=self.especialidad)
        return super().calcular_costo(cantidad, impuesto=impuesto, descuento=descuento)


class CatalogoServicios:
    """Mantiene el catálogo de servicios en memoria durante la ejecución."""

    def __init__(self):
        self._servicios = []

    @property
    def servicios(self):
        return tuple(self._servicios)

    def agregar(self, servicio):
        """Agrega un servicio válido y evita registrar identificadores repetidos."""
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere un objeto Servicio.")
        if any(s.id == servicio.id for s in self._servicios):
            raise DatosInvalidosError("El servicio ya está registrado.")
        self._servicios.append(servicio)
        LOGGER.info("Servicio agregado: %s", servicio.nombre)
        return servicio

    def buscar(self, identificador):
        """Busca un servicio por identificador."""
        for servicio in self._servicios:
            if servicio.id == identificador:
                return servicio
        LOGGER.error("Búsqueda de servicio fallida; ID inexistente: %s", identificador)
        raise LookupError(f"Servicio inexistente: {identificador}")
