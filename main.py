import string
import json
import re
from os import SEEK_SET 


# Path strings
PATH_TO_INPUT_FORMAT_FILE="input/input_format.json"
IGNORE_COLUMNS= {"id_persona_dw"}
DATASET_PATH= "assets/testDatasets/regex_test_dataset.csv"
# DATASET_PATH = "input/datos_nomivac_parte1.csv"
BROKEN_DATA_PATH = "output/broken_data.csv"

# misc constants
REPETITION_TO_NORMALIZE = 30


def check_state_of_fields(fields:list[str], headers:list[str], frequency_map:set[dict[str, str]]) -> str:
    # possible_state_of_fields
    # El profe dijo que no podiamos tener loosey goosey strings so... ¯\_(ツ)_/¯
    CLEAR = "Clear"
    SIZE_ERROR = "Size Mismatch between fields and headers; "
    LIST_ERROR = "Value wasn't find in list; "
    LISTS_ERROR = "Value wasn't find in lists; "
    REGEX_ERROR = "Value didn't match regex in input; "
    RANGE_ERROR = "Value out of range; "

    return_string = ""

    with open(PATH_TO_INPUT_FORMAT_FILE, "r") as input_format:
        input_format = json.loads(input_format.read())
        if len(fields) != len(headers):
            return SIZE_ERROR 
        
        for field_index in range(0, len(fields)):
            field = fields[field_index]
            header = headers[field_index]
            if IGNORE_COLUMNS.__contains__(header):
                continue
            # catch if its not defined
            # TODO: Reformat error message
            if frequency_map[header][field] < REPETITION_TO_NORMALIZE:
                if input_format[header]["type"] == "list":
                    domain = input_format[header]["list"]
                    if (domain.count(field) == 0):
                        return_string += LIST_ERROR + " header: " + header + " field: " + field 
                if input_format[header]["type"] == "lists":
                    domains = input_format[header]["lists"]
                    for domain in domains:
                        if domain.count(field) != 0:
                            break
                    return_string += LISTS_ERROR
                if input_format[header]["type"] == "regex":
                    regex = input_format[header]["regex"]
                    if(re.match(field, regex)):
                        return_string += REGEX_ERROR
                if input_format[header]["type"] == "range":
                    lower_bound = int(input_format[header]["lower_bound"])
                    upper_bound = int(input_format[header]["upper_bound"])
                    # TODO: handle exception if input_format[header]["lower_bound"] is not parseable
                    if lower_bound > int(field) or upper_bound < int(field):
                       return_string = return_string + RANGE_ERROR
        if return_string == "":
            return CLEAR
        return return_string

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
        line_count = 0
        for line in file:
            if line == headers_row:
                continue
            fields = line.split(',')
            for field_index in range(0, len(fields)):
                fields[field_index] = fields[field_index].strip()
            for header_index in range(0, len(headers)):
                # obtener header e ignorar si esta dentro del set de identificadores unicos
                header = headers[header_index]
                if IGNORE_COLUMNS.__contains__(header):
                    continue

                field = fields[header_index]
                if not field in frequency_map[header]:
                    frequency_map[header][field] = 0
                frequency_map[header][field] += 1




        with open(BROKEN_DATA_PATH, "w") as broken_data_file:
            broken_data_file.write("")
        with open(BROKEN_DATA_PATH, "a") as broken_data_file:
            broken_data_file.write(headers_row.strip() + ",OBSERVACIONES\n")
            line_count = 0
            file.seek(0, SEEK_SET)
            for line in file:
                if line == headers_row:
                    continue
                fields = line.split(',')
                for field_index in range(0, len(fields)):
                    fields[field_index] = fields[field_index].strip()

                state_of_line = check_state_of_fields(fields,  headers, frequency_map)
                if state_of_line != "Clear":
                    broken_data_file.write(line.strip() + "," + state_of_line + "\n")
