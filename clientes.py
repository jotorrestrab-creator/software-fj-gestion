"""Gestión de clientes con validación y encapsulación."""
import re
from entidades import Entidad
from excepciones import DatosInvalidosError
from logger_config import LOGGER

class Cliente(Entidad):
    def __init__(self, nombre, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        patron = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        if not isinstance(valor, str) or not re.fullmatch(patron, valor.strip()):
            raise DatosInvalidosError("Correo electrónico inválido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[+0-9()\- ]{7,20}", valor):
            raise DatosInvalidosError("Teléfono inválido.")
        if len(re.sub(r"\D", "", valor)) < 7:
            raise DatosInvalidosError("El teléfono debe tener al menos 7 dígitos.")
        self._telefono = valor.strip()

    def resumen(self):
        return f"{self.nombre} | {self.correo} | {self.telefono}"

class GestorClientes:
    def __init__(self):
        self._clientes = []

    @property
    def clientes(self):
        return tuple(self._clientes)

    def registrar(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere un objeto Cliente.")
        if any(c.correo == cliente.correo for c in self._clientes):
            raise DatosInvalidosError("Ya existe un cliente con ese correo.")
        self._clientes.append(cliente)
        LOGGER.info("Cliente registrado: %s (%s)", cliente.nombre, cliente.id)
        return cliente

    def buscar(self, identificador):
        for cliente in self._clientes:
            if cliente.id == identificador:
                return cliente
        raise LookupError(f"Cliente inexistente: {identificador}")
