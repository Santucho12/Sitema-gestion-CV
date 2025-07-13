
# sistema gestion cv

App web hecha en flask para manejar los curriculums y datos de los que se quieren sumar al equipo de Boston

## como instalar

1. baja la carpeta o clona el repo,
2. arma un entorno virtual de python,
3. instala todo lo que hace falta con:
   pip install -r requirements.txt
4. pone tus datos en el archivo .env, ahi van las claves y todo lo importante
5. asegurate que mysql este andando y la base este creada
6. para arrancar la app, pone:
   python app.py

## que podes hacer
- cargar personas con su cv y foto,
- ver el panel admin, filtrar, ordenar y buscar
- bajar los archivos y ver las fotos antes de descargar
- el admin entra con usuario y contraseña,
- cuando borras gente, se limpian los archivos que ya no sirven

## como esta armado
- app.py: arranca todo y conecta los archivos
- config.py:la data importante
- auth.py: para que no entren usuarios que no deberian tener accesso
- db.py: conecta con la db
- utils.py: funciones para utilizar
- requirements.txt: lo que tenes que instalar
- uploads/: aca se guardan los archivos
- .env: datos privados, no lo subas
- .gitignore: para que no se suba lo que no va

## cosas a tener en cuenta
- si borras la carpeta uploads, se borran los archivos subidos
- si queres mas usuarios, metelos en auth.py
- cualquier cosa que no entiendas preguntame
