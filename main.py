import string
import json


# yanked from https://stackoverflow.com/questions/41105733/limit-ram-usage-to-python-program
import resource
import sys

def memory_limit_half():
    """Limit max memory usage to half."""
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    # Convert KiB to bytes, and divide in two to half
    resource.setrlimit(resource.RLIMIT_AS, (int(get_memory() * 1024 / 2), hard))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory  # KiB



PATH_TO_INPUT_FORMAT_FILE="input/input_format.json"
IGNORE_COLUMNS= {"id_persona_dw"}
DATASET_PATH= "assets/testDatasets/modelo_muestra.csv"
DATASET_PATH = "input/datos_nomivac_parte2.csv"
# PATH_TO_BROKEN_D= "output/broken_data.csv"

def check_state_of_fields(fields:list[str], headers:list[str], frequency_map:set[dict[str, str]]) -> str:
    # possible_state_of_fields
    # El profe dijo que no podiamos tener loosey goosey strings so... ¯\_(ツ)_/¯
    CLEAR = "Clear"
    SIZE_ERROR = "Size Mismatch between fields and headers"
    LIST_ERROR = "Value wasn't find in list"
    LISTS_ERROR = "Value wasn't find in lists"
    REGEX_ERROR = "Value didn't match regex in input"
    RANGE_ERROR = "Value out of range"

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
                # if input_format[header]["type"] == "regex":
                #     regex = input_format[header]["regex"]
                #     if(regex.match(field)):
                #         return_string += REGEX_ERROR
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

    memory_limit_half()

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
        
        line_number = 1
        for line in file:
            line_number += 1
            if line_number%10000==0:
                print("passed line", line_number)
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

                # si len(fields) > len(headers) guardar line en output/broken_data/large_data + OBSERVACIONES
                if len(fields) > len(headers):
                    # TODO: anadir anadir row to large_data y crear large_data
                    continue
                # si len(fields) < len(headers) guardar line en output/broken_data/short_data + OBSERVACIONES
                if len(fields) < len(headers):
                    # TODO: anadir row a short_data
                    continue
                # si len(fields) == len(headers) proceder
                # state_of_line = check_state_of_fields(fields,  headers)
                # if state_of_line != "Clean":
                #     # TODO: add to output/broken_data/bad_format
                #     pass
                


                field = fields[header_index]
                if not field in frequency_map[header]:
                    frequency_map[header][field] = 0
                frequency_map[header][field] += 1

                
        with open("input/datos2_freq_map", "w") as f:
            f.write(frequency_map.__str__())