"""Entidad abstracta general del sistema."""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4

class Entidad(ABC):
    def __init__(self):
        self._id = str(uuid4())
        self._creado_en = datetime.now(timezone.utc)

    @property
    def id(self):
        return self._id

    @property
    def creado_en(self):
        return self._creado_en

    @abstractmethod
    def resumen(self):
        """Devuelve un resumen legible de la entidad."""
