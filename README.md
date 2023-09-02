# restaurant-backend
Restaurant System

## Project Status

En desarrollo

## Installation

A continuación se detallan los pasos para configurar el proyecto en un entorno local.

```bash

# Requirements Backend
* python == 3.9.13

# Clonar el repositorio
git clone https://github.com/reyalexander/restaurant-backend.git

# Navegar al directorio del proyecto
cd restaurant-backend

# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual Windows
venv/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt

# Hacer las migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusario
python manage.py createsuperuser

# Ejemplo de cómo ejecutar el proyecto
python manage.py runserver


## Estructura del Proyecto
inventario-backend/
|-- apps/
    |-- product/
    |-- product_type/
    |-- resource/
    |-- table/
    |-- ticket/
    |-- ticket_detail/
    |-- user/   
|-- restaurant/
|-- .gitignore
|-- manage.py
|-- README.md
|-- requirements.txt

```

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details