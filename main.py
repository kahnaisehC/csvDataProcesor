import string
import json


PATH_TO_INPUT_FORMAT_FILE="input/input_format.json"
columns_to_ignore = {"id_persona_dw"}
DATASET_PATH= "assets/testDatasets/modelo_muestra.csv"
DATASET_PATH = "input/datos_nomivac_parte1.csv"
# PATH_TO_BROKEN_D= "output/broken_data.csv"

def check_state_of_fields(fields:list[str], headers:list[str]) -> str:
    with open(PATH_TO_INPUT_FORMAT_FILE, "r") as input_format:
        input_format = json.loads(input_format.read())
        if len(fields) != len(headers):
            return "Size mismatch between headers and fields"
        
        
        for field_index in range(0, len(fields)):
            field = fields[field_index]
            header = headers[field_index]
            if input_format[header] == "list":
                if input_format[header]["list"].__contains__(field):
                    return ""
                pass
            if input_format[header] == "lists_list":
                pass
            if input_format[header] == "regex":
                pass
            if input_format[header] == "range":
                pass

        return "Clear"

if __name__ == "__main__":


    with open(DATASET_PATH, "r") as file:

        # leer csv headers
        headers_row = file.readline()
        headers = headers_row.split(",")
        for i in range(0, len(headers)):
            headers[i] = headers[i].strip()

        # crear frequency map de los identificadores no unicos  
        # NOTE: uso "for i in range(0, len(it)) porque necesito modificar los elementos del iterable"
        # NOTE: en cambio, "for i in it" trata a 'i' como una copia y no como referencia por lo que no es suitable para este caso"
        frequency_map = {}
        for header in headers:
            frequency_map[header] = {}
        for line in file:
            if line == headers_row:
                continue
            fields = line.split(',')
            for field_index in range(0, len(fields)):
                fields[field_index] = fields[field_index].strip()
            for header_index in range(0, len(headers)):
                # obtener header e ignorar si esta dentro del set de identificadores unicos
                header = headers[header_index]
                if columns_to_ignore.__contains__(header):
                    continue

                # si len(fields) > len(headers) guardar line en output/broken_data/large_data + OBSERVACIONES
                if len(fields) > len(headers):
                    # TODO: anadir anadir row to large_data y crear large_data
                    continue
                # si len(fields) < len(headers) guardar line en output/broken_data/short_data + OBSERVACIONES
                if len(fields) < len(headers):
                    # TODO: anadir row a short_data
                    continue
                # si len(fields) == len(headers) proceder
                state_of_line = check_state_of_fields(fields,  headers)
                if state_of_line != "Clean":
                    # TODO: add to output/broken_data/bad_format
                    pass
                


                field = fields[header_index]
                if not field in frequency_map[header]:
                    frequency_map[header][field] = 0
                frequency_map[header][field] += 1

        with open("input/datos1_freq_map", "w") as f:
            f.write(frequency_map.__str__())