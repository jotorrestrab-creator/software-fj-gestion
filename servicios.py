""""Servicios abstractos y especializados."""
from abc import abstractmethod
from decimal import Decimal, InvalidOperation
from entidades import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError
from logger_config import LOGGER

def decimal_positivo(valor, campo):
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise DatosInvalidosError(f"{campo} debe ser numérico.") from exc
    if not numero.is_finite() or numero <= 0:
        raise DatosInvalidosError(f"{campo} debe ser mayor que cero.")
    return numero

class Servicio(Entidad):
    def __init__(self, nombre, tarifa_base):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        self.nombre = nombre.strip()
        self.tarifa_base = decimal_positivo(tarifa_base, "La tarifa")
        self._disponible = True

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser booleana.")
        self._disponible = disponible
        LOGGER.info("Disponibilidad de %s: %s", self.nombre, disponible)

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Servicio no disponible: {self.nombre}")

    def calcular_costo(self, cantidad=1, *, impuesto=0, descuento=0):
        """Calcula costo con cantidad, impuesto y descuento opcionales."""
        unidades = decimal_positivo(cantidad, "La cantidad")
        tasa, rebaja = Decimal(str(impuesto)), Decimal(str(descuento))
        if not tasa.is_finite() or not Decimal("0") <= tasa <= Decimal("1"):
            raise DatosInvalidosError("Impuesto fuera del rango 0..1.")
        if not rebaja.is_finite() or not Decimal("0") <= rebaja <= Decimal("1"):
            raise DatosInvalidosError("Descuento fuera del rango 0..1.")
        total = self.tarifa_base * unidades * (1 - rebaja) * (1 + tasa)
        return total.quantize(Decimal("0.01"))

    @abstractmethod
    def describir(self):
        """Describe el servicio concreto."""

    @abstractmethod
    def validar_parametros(self, **parametros):
        """Valida parámetros propios del servicio."""

    def resumen(self):
        return f"{self.describir()} | tarifa ${self.tarifa_base}"

class ServicioSala(Servicio):
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

class ServicioEquipo(Servicio):
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

class ServicioAsesoria(Servicio):
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

class CatalogoServicios:
    def __init__(self):
        self._servicios = []

    @property
    def servicios(self):
        return tuple(self._servicios)

    def agregar(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere un objeto Servicio.")
        if any(s.id == servicio.id for s in self._servicios):
            raise DatosInvalidosError("El servicio ya está registrado.")
        self._servicios.append(servicio)
        LOGGER.info("Servicio agregado: %s", servicio.nombre)
        return servicio

    def buscar(self, identificador):
        for servicio in self._servicios:
            if servicio.id == identificador:
                return servicio
        raise LookupError(f"Servicio inexistente: {identificador}")
"