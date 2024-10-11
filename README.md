# Language/Idioma

1. [English](#index)
2. [Español](#índice)

# INDEX

1. [Description](#csv-data-procesor-script).
2. [Features](#features).
3. [Requirements](#requirements).
4. [Usage](#usage).
5. [How It Works](#how-it-works).
6. [Input Format](#customizing-the-filtering-rules).
7. [Assignments](#answers-to-the-asignment).
8. [Author](#author).
9. [Tests](#tests).

# CSV Data Procesor Script

This Python script reads a `.csv` file, processes its content, and filters out rows with broken data while also implementing a function to query against the given dataset. 

## Features
- Reads data from a CSV file.
- Detects and filters out broken or invalid data (e.g., missing fields, incorrect data types, etc.).
- Outputs the broken data rows with an explanation to why they were considered broken.

## Requirements
- Python 3.x

## Usage

1. Place your CSV file in the input folder with the "dataset.csv" name.

2. Place your input format in the input_format.json. To learn more about the input format go to [Customizing the filtering Rules](#customizing-the-filtering-rules).

3. Run the script with the following command:

```bash
$ python main.py
```

## How It Works

1. **Read the CSV File**: The script loads the data from the provided `.csv` file.
   
2. **Data Validation**: The script checks for broken or invalid data.

3. **Write Broken Data**: The script writes the broken data in the output/broken_data.csv file.

4. **Execute the Queries**: The script executes some hardcoded queries. The results of these queries are stored in output/requested_data.txt
   
## Customizing the Filtering Rules

This script accepts only a custom format. The format accepts three types of fields to filter the dataset:

- list: defined as:
```js
    "field-name1":{
        "type": "list",
        "list": [
        "list",
        "of",
        "values",
        "in",
        "the",
        "domain"
    ]}
```
this type of format will filter every record which field value doesn't appear on the list OR the occurrences of the value are less than the set in the constant REPETITION_TO_NORMALIZE.
- regex: defined as:
```js
    "field-name2": {
        "type": "regex",
        "regex": "^/d?r*[eE3]g+ex$"
    }
```
this type of format will filter every record which field value doesn't match the regex.
- range: defined as:
```js
    "field-name3": {
        "type": "range",
        "lower_bound": 0,
        "upper_bound": 100,
        "NOTE": "these are INCLUDING bounds(from 0 to 100 including)"
    }
```
this type of format will filter every record which field value isn't inside the specified range. Note that these are INCLUDING bounds, meaning that, in this example, 0 and 100 match this format.


## Answers to the asignment
The answers to the assignments will be stored in docs/output alongside a pdf docs/respuesta.pdf that clarifies and analyses these files.
Note that the docs/output folder is for the "datos_nomivac_parte1.csv", while the docs/output2 folder is for the "datos_nomivac_parte2.csv". Both of them present the same structure tho.
Inside the docs/output folder there will be: 
1. broken_data.csv: a file that contains every record that presents some kind of inconsistency, the "OBSERVACIONES" header serves as an explanation to why these record was selected. 
2. requested_data.csv: a file that contains raw the assignments that were requested respectively. The data inside this file is further explained in docs/respuesta.pdf

## Author

[Ian Hakanson]

## Tests

The tests are in progress... 
There is the testDatasets folder where you can find the test datasets alongside the test outputs that will be used for the unittest.

# ÍNDICE

1. [Descripción](#script-procesador-de-datos-csv).
2. [Funcionalidades](#funcionalidades).
3. [Requisitos](#requisitos).
4. [Uso](#uso).
5. [Cómo funciona](#cómo-funciona).
6. [Formato de Entrada](#personalizar-las-reglas-de-filtrado).
7. [Desafío Integrador](#respuestas-al-desafío-integrador).
8. [Autor](#autor).
9. [Tests](#tests-1).

# Script Procesador de Datos CSV

Este script de Python lee un archivo `.csv`, procesa su contenido y filtra las filas con datos corruptos, además de implementar una función para realizar consultas sobre el conjunto de datos dado.

## Funcionalidades
- Lee datos de un archivo CSV.
- Detecta y filtra datos rotos o inválidos (por ejemplo, campos faltantes, tipos de datos incorrectos, etc.).
- Genera un archivo con los datos rotos junto con una explicación de por qué se consideraron defectuosos.

## Requisitos
- Python 3.x

## Uso

1. Coloca tu archivo CSV en la carpeta de entrada con el nombre `dataset.csv`.

2. Coloca tu formato de entrada en el archivo `input_format.json`. Para aprender más sobre el formato de entrada, consulta [Personalizar las Reglas de Filtrado](#personalizar-las-reglas-de-filtrado).

3. Ejecuta el script con el siguiente comando:

```bash
$ python main.py
```

## Cómo Funciona

1. **Leer el Archivo CSV**: El script carga los datos del archivo `.csv` proporcionado.
   
2. **Validación de Datos**: El script revisa si hay datos rotos o inválidos.

3. **Escribir los Datos Corruptos**: El script escribe los datos rotos en el archivo `output/broken_data.csv`.

4. **Ejecutar las Consultas**: El script ejecuta algunas consultas predefinidas. Los resultados de estas consultas se almacenan en `output/requested_data.txt`.
   
## Personalizar las Reglas de Filtrado

Este script acepta solo un formato personalizado. El formato admite tres tipos de campos para filtrar el conjunto de datos:

- **lista**: definido como:
```js
    "nombre-campo1": {
        "type": "list",
        "list": [
        "lista",
        "de",
        "valores",
        "en",
        "el",
        "dominio"
    ]}
```
Este tipo de formato filtrará cualquier registro cuyo valor en el campo no aparezca en la lista O si las ocurrencias del valor son menores a las definidas en la constante `REPETITION_TO_NORMALIZE`.

- **regex**: definido como:
```js
    "nombre-campo2": {
        "type": "regex",
        "regex": "^/d?r*[eE3]g+ex$"
    }
```
Este tipo de formato filtrará cualquier registro cuyo valor en el campo no coincida con la expresión regular (regex).

- **rango**: definido como:
```js
    "nombre-campo3": {
        "type": "range",
        "lower_bound": 0,
        "upper_bound": 100,
        "NOTE": "estos son límites INCLUSIVOS (de 0 a 100, incluyendo)"
    }
```
Este tipo de formato filtrará cualquier registro cuyo valor en el campo no esté dentro del rango especificado. Ten en cuenta que estos límites son INCLUSIVOS, lo que significa que, en este ejemplo, tanto 0 como 100 coinciden con este formato.

## Respuestas al desafío integrador

Las respuestas al desafío integrador se almacenarán en `docs/output`, junto con un archivo PDF `docs/respuesta.pdf` que clarifica y analiza estos archivos.
Ten en cuenta que la carpeta `docs/output` corresponde a los datos del archivo "datos_nomivac_parte1.csv", mientras que la carpeta `docs/output2` corresponde a "datos_nomivac_parte2.csv". Ambas carpetas presentan la misma estructura.

Dentro de la carpeta `docs/output` encontrarás:

1. **broken_data.csv**: Un archivo que contiene cada registro que presenta algún tipo de inconsistencia. El encabezado "OBSERVACIONES" sirve como explicación de por qué se seleccionó dicho registro.
2. **requested_data.csv**: Un archivo que contiene las asignaciones solicitadas. Los datos dentro de este archivo se explican más a fondo en `docs/respuesta.pdf`.

## Autor

[Ian Hakanson]

## Tests

Los tests están en proceso...
En la carpeta testDatasets podés encontrar los datasets junto con sus respectivas salidas que van a ser utilizadas para el unittest.