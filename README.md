### HOW TO USE
The dataset goes in the input directory
The datasets that are in the assets/testDataSets are necessary for the tests.py to run correctly

dentro de la carpeta input se debe proporcionar un input_format para determinar como se van a procesar los fields de los datos. El archivo input_format_example muestra las opciones sobre como escribir el formato de los fields
**TENES** que poner el "type" **DE MANERA OBLIGATORIA**
el valor "criticity" es una variable que ayuda a la hora de organizar los datos rotos. Si un field tiene baja criticidad y esta "roto" (no cumple con las condiciones en el input_format.json o si tiene muy baja frecuencia) puede ser que el record al que pertenece se  utilice para el analisis sin importar 

si el nombre de un field no esta en el input_json se mostrara un mensaje por consola y se procedera suponiendo que ese field puede tener cualquier valor 


El archivo "input_format" exportado es el que se debe usar para los dataset 1 y 2 

### Respuestas a las consignas
Las respuestas a las consignas van a estar guardadas en la carpeta output

