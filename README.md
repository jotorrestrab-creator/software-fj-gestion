# Software FJ — Gestión de clientes, servicios y reservas

Proyecto académico de Programación (213023), Fase 4 – Prácticas simuladas, UNAD.

Aplicación en Python con programación orientada a objetos y una interfaz gráfica de escritorio desarrollada con Tkinter.

## Requisitos
- Python 3.10 o superior.
- Tkinter (incluido habitualmente en las instalaciones estándar de Python).
- No requiere paquetes externos adicionales.

## Ejecución
Desde la carpeta raíz del proyecto:

```bash
python -X utf8 interfaz.py
```

Se abrirá la interfaz gráfica con las pestañas Clientes, Servicios y Reservas. También se conserva la demostración por consola:

```bash
python -X utf8 main.py
python -X utf8 pruebas.py
```

La batería automatizada contiene 28 escenarios positivos y negativos.

## Funciones de la interfaz
- **Clientes:** registrar clientes con validación de nombre, correo y teléfono.
- **Servicios:** agregar salas, alquiler de equipos y asesorías con sus parámetros específicos.
- **Reservas:** crear reservas, confirmarlas, procesarlas y cancelarlas.
- **Validaciones:** mostrar errores controlados mediante ventanas emergentes.
- **Registro:** conservar los eventos y errores técnicos en `logs/sistema.log`.

Al iniciar, se cargan diez servicios de demostración: tres espacios (Sala Norte, Sala de reuniones y Auditorio principal), cuatro equipos (Proyector, Computador portátil, Equipo de sonido y Cámara de video) y tres asesorías (Python, empresarial y tecnológica).

## Estructura
- `entidades.py`: clase abstracta base Entidad.
- `clientes.py`: Cliente, validaciones y gestor de clientes.
- `servicios.py`: clase abstracta Servicio, tres especializaciones y catálogo.
- `reservas.py`: reservas, estados y transiciones.
- `excepciones.py`: excepciones personalizadas y registro de errores del dominio.
- `logger_config.py`: configuración del registro de eventos.
- `main.py`: demostración por consola.
- `interfaz.py`: interfaz gráfica de escritorio con Tkinter.
- `pruebas.py`: batería de 28 escenarios.
- `docs/ESCENARIOS_DE_PRUEBA.md`: matriz de pruebas.

## Reglas de funcionamiento y alcance
- Clientes, servicios y reservas se gestionan en objetos y listas durante la ejecución. Al cerrar la aplicación, la información operativa se reinicia; no se usa base de datos ni almacenamiento persistente.
- No se utiliza base de datos.
- Los datos operativos se pierden al cerrar la aplicación; el archivo de log no es almacenamiento de datos de negocio.
- Los servicios especializados redefinen `calcular_costo` y aplican sus validaciones particulares.
- La función de cálculo acepta parámetros opcionales de impuesto y descuento como variante de cálculo.

## Pruebas
Los resultados esperados de los 28 escenarios están documentados en `docs/ESCENARIOS_DE_PRUEBA.md`. Una prueba negativa es satisfactoria cuando el sistema rechaza la operación mediante una excepción controlada y continúa ejecutando las demás pruebas.
