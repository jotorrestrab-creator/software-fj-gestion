# Diseño técnico y correspondencia con los componentes

## Componentes implementados

| Componente | Archivo | Responsabilidad |
|---|---|---|
| Entidad abstracta | `entidades.py` | Identificador, fecha de creación y contrato de resumen |
| Cliente | `clientes.py` | Datos validados, encapsulación y gestión en memoria |
| Servicio abstracto | `servicios.py` | Tarifa, disponibilidad y cálculo de costos |
| ServicioSala | `servicios.py` | Servicio especializado con capacidad |
| ServicioEquipo | `servicios.py` | Servicio especializado con unidades disponibles |
| ServicioAsesoria | `servicios.py` | Servicio especializado por área de conocimiento |
| Reserva | `reservas.py` | Cliente, servicio, duración, valor y estado |
| Excepciones | `excepciones.py` | Errores específicos del dominio |
| Registro de eventos | `logger_config.py` | Archivo de eventos y errores |
| Pruebas | `pruebas.py` | Quince escenarios reproducibles |

## Conceptos de POO

- **Abstracción:** `Entidad` y `Servicio` definen contratos abstractos.
- **Herencia:** `Cliente` y `Servicio` derivan de `Entidad`; los tres tipos de servicio derivan de `Servicio`.
- **Encapsulación:** los datos del cliente se exponen mediante propiedades que validan los valores antes de asignarlos.
- **Polimorfismo:** cada clase concreta de servicio implementa `describir` y `validar_parametros` de acuerdo con sus características.

## Variantes de cálculo

Python no implementa sobrecarga tradicional por firma como Java. Para ofrecer distintas formas de cálculo, el método `calcular_costo` utiliza parámetros opcionales y nombrados: cantidad, impuesto y descuento. Esto permite calcular una tarifa básica, varias unidades, aplicar impuesto o descuento y combinar los parámetros.

## Manejo de excepciones

- `try/except`: control de errores durante el registro y la demostración.
- `try/except/else`: confirma la operación cuando no ocurre una excepción.
- `try/except/finally`: registra el cierre del intento de procesamiento, haya o no error.
- **Encadenamiento:** se utiliza `raise ... from exc` para conservar la causa original de una conversión o cálculo fallido.

## Alcance y límites

Los datos de clientes, servicios y reservas permanecen en memoria durante la ejecución. El archivo de logs registra eventos técnicos; no es una base de datos ni mecanismo de persistencia de los registros funcionales.
