# Portal de Postulación con Flask

## Descripción

Aplicación web para que usuarios suban su Currículum Vitae (CV) mediante un formulario. Los CVs se almacenan en el servidor y la información se guarda en una base de datos MySQL. Incluye un panel administrativo protegido para revisar postulantes y acceder a sus CVs.

## Tecnologías

- Python 3.x
- Flask
- MySQL
- HTML, CSS, JavaScript

## Estructura del proyecto

```
/
├── app.py
├── templates/
│   ├── form.html
│   └── admin.html
├── static/
│   ├── styles.css
│   └── stylesAdmin.css
├── uploads/
├── .env
├── requirements.txt
└── README.md
```

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto con tus datos de configuración.
2. Crea la base de datos y la tabla de postulantes en MySQL:

```sql
CREATE DATABASE postulantes_db;

USE postulantes_db;

CREATE TABLE postulantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    nombre_archivo_cv VARCHAR(255)
);
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

- Ejecuta la aplicación con `python app.py`.
- Accede al formulario en [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
- Sube CV en formato `.pdf`, `.doc`, `.docx`.
- El panel administrativo está protegido y permite revisar postulantes.

## Notas

- No subi el archivo `.env` al repositorio.
- oculte la carpeta `uploads` .

