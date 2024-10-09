import json
import re



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
DATASET_PATH= "assets/testDatasets/range_test_dataset.csv" 
# DATASET_PATH = "input/datos_nomivac_parte1.csv"
BROKEN_DATA_PATH = "output/broken_data.csv"
# BROKEN_DATA_PATH = "assets/testDatasets/list_test_output.csv"

# misc constants
REPETITION_TO_NORMALIZE = 2

def process_error_string(error: str, field: str, header: str) -> str:
    return error + "field: " + field + ". header: " + header

def check_state_of_fields(fields:list[str], headers:list[str], frequency_map:set[dict[str, str]]) -> str:
    # possible_state_of_fields
    # El profe dijo que no podiamos tener loosey goosey strings so... ¯\_(ツ)_/¯
    CLEAR = "Clear"
    SIZE_ERROR = " Size Mismatch between fields and headers; "
    LIST_ERROR = " Value has not been found in list; "
    LISTS_ERROR = " Value has not been found in lists; "
    REGEX_ERROR = " Value didn't match regex in input; "
    OUT_OF_RANGE_ERROR = " Value out of range; "
    NAN_RANGE_ERROR = " Value is not a number; "
    LOWER_UPPER_RANGE_ERROR = " Lower or Upper bound is not defined as an int. check input/input_format.json "

    return_string = ""

    return_string = ""

    with open(PATH_TO_INPUT_FORMAT_FILE, "r") as input_format:
        input_format = json.loads(input_format.read())
        if len(fields) != len(headers):
            return SIZE_ERROR 
        
        for field_index in range(0, len(fields)):
            field = fields[field_index]
            header = headers[field_index]


            if input_format[header]["type"] == "list" and frequency_map[header][field] < REPETITION_TO_NORMALIZE:
                domain = input_format[header]["list"]
                if (domain.count(field) == 0):
                    return_string += process_error_string(LIST_ERROR, field, header) 
            if input_format[header]["type"] == "lists" and frequency_map[header][field] < REPETITION_TO_NORMALIZE:
                domains = input_format[header]["lists"]
                for domain in domains:
                    if domain.count(field) != 0:
                        break
                return_string += process_error_string(LISTS_ERROR, field, header)
            if input_format[header]["type"] == "regex":
                regex = input_format[header]["regex"]
                r = re.compile(regex)
                if(r.match(field) == None):
                    return_string += process_error_string(REGEX_ERROR, field, header) 
            if input_format[header]["type"] == "range":
                lower_bound = int(input_format[header]["lower_bound"])
                upper_bound = int(input_format[header]["upper_bound"])
                if field.isdigit() == False:
                    return_string += process_error_string(NAN_RANGE_ERROR, field, header)
                elif (lower_bound.__class__ != int
                      or upper_bound.__class__ != int
                    ):
                    return_string += process_error_string(LOWER_UPPER_RANGE_ERROR, field, header)
                elif (lower_bound > int(field)
                    or upper_bound < int(field)
                    ):
                    return_string += process_error_string(OUT_OF_RANGE_ERROR, field, header) 


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
        line_count = 0
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

                field = fields[header_index]
                if not field in frequency_map[header]:
                    frequency_map[header][field] = 0
                frequency_map[header][field] += 1



    with open(DATASET_PATH, "r") as file:
        with open(BROKEN_DATA_PATH, "w") as broken_data_file:
            broken_data_file.write("")
        with open(BROKEN_DATA_PATH, "a") as broken_data_file:
            broken_data_file.write(headers_row.strip() + ",OBSERVACIONES\n")
            for line in file:
                if line == headers_row:
                    continue
                fields = line.split(',')
                for field_index in range(0, len(fields)):
                    fields[field_index] = fields[field_index].strip()

                state_of_line = check_state_of_fields(fields,  headers, frequency_map)
                if state_of_line != "Clear":
                    broken_data_file.write(line.strip() + "," + state_of_line + "\n")
