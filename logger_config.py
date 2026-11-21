"""Configuración de logs."""
import logging
from pathlib import Path

def obtener_logger(nombre="software_fj"):
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    carpeta = Path(__file__).resolve().parent / "logs"
    carpeta.mkdir(parents=True, exist_ok=True)
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    archivo = logging.FileHandler(carpeta / "sistema.log", encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)
    return logger

LOGGER = obtener_logger()
