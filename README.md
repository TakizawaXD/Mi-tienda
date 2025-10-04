
# Proyecto Misión 2

Este proyecto es una aplicación web desarrollada en Python, creada como parte de una misión educativa para el aprendizaje de desarrollo web y bases de datos. El objetivo principal es proporcionar una plataforma sencilla donde los usuarios puedan registrarse, iniciar sesión y gestionar un carrito de compras, simulando el flujo básico de una tienda en línea.

## Propósito del Proyecto

El proyecto fue creado con fines didácticos, pensado para estudiantes o personas interesadas en aprender los fundamentos del desarrollo de aplicaciones web con Python, manejo de plantillas HTML y uso de bases de datos SQLite. Sirve como base para comprender la estructura de una aplicación web real y cómo se integran los diferentes componentes.

## Público Objetivo

Está dirigido principalmente a estudiantes, docentes y autodidactas que buscan un ejemplo práctico y funcional para estudiar, modificar y expandir según sus necesidades. Es ideal para quienes están dando sus primeros pasos en el desarrollo web y desean experimentar con un proyecto completo y funcional.

## Visión y Futuro del Proyecto

Se tiene pensado que este proyecto evolucione incorporando nuevas funcionalidades, como la gestión de productos, integración de métodos de pago, panel de administración y mejoras en la seguridad. La idea es que sirva como punto de partida para proyectos más complejos o como base para prácticas y evaluaciones académicas.

## Estructura del Proyecto

- `app.py`: Archivo principal de la aplicación.
- `models.py`: Modelos de datos y lógica de base de datos.
- `schemas.py`: Esquemas de validación y serialización.
- `requirements.txt`: Dependencias del proyecto.
- `instance/database.db`: Base de datos SQLite utilizada por la aplicación.
- `templates/`: Plantillas HTML para la interfaz de usuario.
- `__pycache__/`: Archivos compilados de Python.

## Instalación

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## Uso

- Accede a la aplicación desde tu navegador en la dirección que indique la consola (por defecto suele ser `http://127.0.0.1:5000/`).
- Regístrate, inicia sesión y utiliza el carrito de compras.

## Ejemplo de la Base de Datos

La base de datos se encuentra en `instance/database.db` y contiene las siguientes tablas principales:

### Tabla: User
| id | username | email           | password_hash      |
|----|----------|-----------------|-------------------|
| 1  | juan     | juan@mail.com   | (hash)            |
| 2  | maria    | maria@mail.com  | (hash)            |

### Tabla: Product
| id | name         | description         | price | image         | stock |
|----|--------------|--------------------|-------|---------------|-------|
| 1  | Camiseta     | Camiseta de algodón| 15.99 | img1.jpg      | 10    |
| 2  | Pantalón     | Pantalón de mezclilla| 29.99 | img2.jpg    | 5     |

### Tabla: CartItem
| id | user_id | product_id | quantity |
|----|---------|------------|----------|
| 1  | 1       | 2          | 1        |
| 2  | 2       | 1          | 2        |

## Licencia

Este proyecto es de uso educativo y puede ser modificado libremente.
