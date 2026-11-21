# Software FJ — Gestión de clientes, servicios y reservas

Proyecto académico de Programación (213023), Fase 4 – Prácticas simuladas, UNAD.

Aplicación de consola desarrollada en Python con programación orientada a objetos, clases abstractas, herencia, encapsulación, polimorfismo y manejo de excepciones.

## Requisitos
- Python 3.10 o superior.
- No requiere paquetes externos.

## Ejecución
```bash
python main.py
```

Ejecutar los 15 escenarios de prueba:
```bash
python pruebas.py
```

Los eventos se registran en `logs/sistema.log`.

## Estructura
- `entidades.py`: clase abstracta Entidad.
- `clientes.py`: Cliente, validaciones y gestor de clientes.
- `servicios.py`: Servicio abstracto, tres especializaciones y catálogo.
- `reservas.py`: reservas, estados y transiciones.
- `excepciones.py`: excepciones personalizadas.
- `logger_config.py`: configuración de logs.
- `main.py`: recorrido demostrativo.
- `pruebas.py`: 15 escenarios reproducibles.
- `docs/ESCENARIOS_DE_PRUEBA.md`: matriz de pruebas.

## Alcance y limitaciones
La aplicación mantiene clientes, servicios y reservas en memoria durante la ejecución. No utiliza base de datos ni persiste esos registros después de cerrar el programa. El archivo de logs conserva eventos técnicos, no constituye almacenamiento de clientes o reservas.

Los escenarios son simulados y permiten demostrar operaciones correctas y el control de entradas inválidas.
