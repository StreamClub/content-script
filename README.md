# Flujo de recomendaciones

Última actualización 01/06/2024

## Configurar entorno
Crear e iniciar un enviroment para ejecutar los scripts

    $ python -m venv ./myenv

    $ source ./myenv/bin/activate

Instalar dependencias:

    $ pip install -r requirements.txt

# Recomendaciones por contenido

## Calcular Recomendaciones Pelicula-Pelicula y Serie-Serie

### Paso 1: Generar las recomendaciones 
- En Drive, ir a la carpeta Algoritmo de Recomendacion/Notebooks/Calcular recomendaciones
- Ejecutar Notebook "Recomendaciones Pelicula-Pelicula.ipynb" y "Recomendaciones Serie-Serie.ipynb"
- Descargar en archivo movie_movie_recommendation.csv y series_series_recommendation.csv de la carpeta Resultados
- Guardarlo en ./UploadRecosToRDB/

### Paso 2: Subir las recomendaciones a la rdb
Ejecutar los siguientes comandos
```
$ cd UploadRecosToRDB
$ python upload_recos_to_rdb.py <tipo>
```
Donde tipo puede ser "MMR" O "SSR"

# Recomendaciones por usuarios

## Actualizar contenido visto por usuarios para el calculo de recomendaciones

### Paso 1: Descargar historial de contenido visto
Ejecutar los siguientes comandos
```
$ cd LoadSeenContentToCSV
$ python load_seen_content_to_csv.py
```

### Paso 2: Subir las novedades
- Subir el archivo users_seen_content.csv a la carpeta Algoritmo de Recomendacion/Notebooks/Datasets
- Continuar con los pasos del calculo de recomendaciones Usuario-Pelicula y Usuario-Serie

## Calcular Recomendaciones Usuario-Pelicula y Usuario-Serie

### Paso 1: Generar las recomendaciones 
- Ir al Drive/Algoritmo de Recomendacion/.../
- Ejecutar Notebook "Recomendaciones Usuario-Pelicula.ipynb" y "Recomendaciones Usuario-Serie.ipynb"
- Descargar en archivo user_movie_recommendation.csv y user_series_recommendation.csv de la carpeta Resultados
- Guardarlo en ./UploadRecosToRDB/

### Paso 2: Subir las recomendaciones a la rdb
Ejecutar los siguientes comandos
```
$ cd UploadRecosToRDB
$ python upload_recos_to_rdb.py <tipo>
```
Donde tipo puede ser "UMR" O "USR"