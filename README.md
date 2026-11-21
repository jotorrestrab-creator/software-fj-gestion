# Software FJ — Gestión de clientes, servicios y reservas

Proyecto académico de Programación (213023), Fase 4 – Prácticas simuladas, UNAD.

Aplicación de consola en Python que aplica programación orientada a objetos: abstracción, herencia, encapsulamiento, polimorfismo y manejo de excepciones personalizadas.

## Requisitos
- Python 3.10 o superior.
- No requiere paquetes externos.

## Ejecución
Desde la carpeta raíz:

```bash
python main.py
python pruebas.py
```

La batería automatizada contiene 26 escenarios positivos y negativos. Cada escenario se ejecuta de forma aislada para que una excepción esperada no interrumpa los casos posteriores.

## Estructura
- `entidades.py`: clase abstracta base Entidad.
- `clientes.py`: Cliente, validaciones y gestor de clientes.
- `servicios.py`: clase abstracta Servicio, tres especializaciones y catálogo.
- `reservas.py`: reservas, estados y transiciones.
- `excepciones.py`: excepciones personalizadas y registro de errores del dominio.
- `logger_config.py`: configuración del registro de eventos.
- `main.py`: demostración de operaciones.
- `pruebas.py`: batería de 26 escenarios.
- `docs/ESCENARIOS_DE_PRUEBA.md`: matriz de pruebas.

## Reglas de funcionamiento
- Clientes, servicios y reservas se gestionan en objetos y listas durante la ejecución.
- No se utiliza base de datos.
- El archivo `logs/sistema.log` se utiliza exclusivamente para registrar eventos y errores técnicos; no es almacenamiento de datos de negocio.
- Los servicios especializados redefinen `calcular_costo` y aplican sus validaciones particulares antes de delegar el cálculo común.
- La función de cálculo acepta parámetros opcionales de impuesto y descuento. En Python, esta variante con parámetros opcionales permite cubrir el comportamiento de sobrecarga requerido en el ejercicio sin duplicar firmas de método.

## Pruebas
Los resultados esperados de los 26 escenarios están documentados en `docs/ESCENARIOS_DE_PRUEBA.md`. Una prueba negativa es satisfactoria cuando el sistema rechaza la operación mediante una excepción controlada y continúa ejecutando las demás pruebas.

## Alcance y limitaciones
Los datos operativos existen únicamente durante la ejecución y se pierden al cerrar el programa. Los escenarios son simulados y no representan una conexión con servicios externos ni persistencia de reservas.
