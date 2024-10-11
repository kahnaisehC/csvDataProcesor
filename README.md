The datasets that are in the assets/testDataSets are necessary for the tests.py to run correctly

dentro de la carpeta input se debe proporcionar un input_format para determinar como se van a procesar los fields de los datos. El archivo input_format_example muestra las opciones sobre como escribir el formato de los fields
**TENES** que poner el "type" **DE MANERA OBLIGATORIA**
el valor "criticity" es una variable que ayuda a la hora de organizar los datos rotos. Si un field tiene baja criticidad y esta "roto" (no cumple con las condiciones en el input_format.json o si tiene muy baja frecuencia) puede ser que el record al que pertenece se  utilice para el analisis sin importar 

si el nombre de un field no esta en el input_json se mostrara un mensaje por consola y se procedera suponiendo que ese field puede tener cualquier valor 


El archivo "input_format" exportado es el que se debe usar para los dataset 1 y 2

### INDEX

The `README.md` is structured to:
1. Describe the script’s purpose.
2. List the dependencies and how to install them.
3. Provide a clear usage example.
4. Briefly explain how the script works and what kind of filtering it performs.
5. Offer instructions for customizing filtering rules.

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
python main.py
```

## How It Works

1. **Read the CSV File**: The script loads the data from the provided `.csv` file.
   
2. **Data Validation**: The script checks for broken or invalid data.

3. **Write Broken Data**: The script writes the broken data in the output/broken_data.csv file.

4. **Execute the Queries**: The script executes some hardcoded queries. The results of these queries are stored in output/requested_data.txt
   
## Customizing the Filtering Rules



## Answers to the asignment
The answers to the assignments will be stored in docs/output alongside a pdf docs/respuesta.pdf that clarifies and analyses these files.
Note that the docs/output folder is for the "datos_nomivac_parte1.csv", while the docs/output2 folder is for the "datos_nomivac_parte2.csv". Both of them present the same structure tho.
Inside the docs/output folder there will be: 
1. broken_data.csv: a file that contains every record that presents some kind of inconsistency, the "OBSERVACIONES" header serves as an explanation to why these record was selected. 
2. requested_data.csv: a file that contains in raw the assignments that were requested respectively. The data inside this file is further explained in docs/respuesta.pdf

## Author

[Ian Hakanson]

The full project will be hosted on [This Repo](https://github.com/kahnaisehC/csvDataProcesor). Make sure to check it out and feel free to reach out for any questions or issues!


## Tests

