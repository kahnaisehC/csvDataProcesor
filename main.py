import json
import re

# paths to files
PATH_TO_INPUT_FORMAT_FILE="input/input_format.json"
DATASET_PATH= "assets/testDatasets/range_test_dataset.csv" 
# DATASET_PATH = "input/datos_nomivac_parte1.csv"
BROKEN_DATA_PATH = "output/broken_data.csv"
# BROKEN_DATA_PATH = "assets/testDatasets/list_test_output.csv"
OUTPUT_PATH = "output/requested_data.txt"

# misc constants

# amount of repetitions a field value should have to not consider it an error 
# if a field value doesn't appear in its repective list in the input_format.json
REPETITION_TO_NORMALIZE = 30 

# name of the headers that won't appear in the frequency maps
# usually used for unique identifiers in order to not store 
# a ton of crap to memory
IGNORE_COLUMNS= {"id_persona_dw"}


# transforms a comma separated record into a list
# process_line("a,little,record") // ["a", "little", "record"]
def process_record(record: str):
    record = record.split(',')
    for field_index in range(0,len(record)):
        record[field_index] = record[field_index].strip()
    return record

# queries the amount of appearences that has every intersection of the searched_headers in the csv file "path"
def query(path: str, *searched_headers: tuple[str])->dict[str, int]:
    ret = {}
    with open(path, "r") as file:
        headers = []
        header_indexes = []
        for index, record in enumerate(file):
            if index == 0:
                headers = process_record(record)
                for sheader in searched_headers:
                    for header_index, header in enumerate(headers):
                        if header != sheader:
                            continue
                        header_indexes.append(header_index)
                        break
                continue
            fields = process_record(record)

            if check_state_of_fields(fields, headers, frequency_map) != 'Clear':
                continue
            list_of_values = ""
            for header_index in header_indexes:
                list_of_values += fields[header_index] + ","
            
            if not list_of_values in ret:
                ret[list_of_values] = 0
            
            ret[list_of_values] += 1


    return ret


# helper function to concatenate an incompatibility message, field and header in a clean way
def process_error_string(error: str, field: str, header: str) -> str:
    return error + "field: " + field + ". header: " + header


# check if the state of a field is broken (doesn't match the input format or if it has more or less rows than the headers)
# if the record is fine, returns "Clear", otherwise returns an error string with the found incompatibilities

def check_state_of_fields(fields:list[str], headers:list[str], frequency_map:set[dict[str, str]]) -> str:
    # El profe dijo que no podiamos tener loosey goosey strings so... ¯\_(ツ)_/¯
    CLEAR = "Clear"
    SIZE_ERROR = " Size Mismatch between fields and headers; "
    LIST_ERROR = " Value has not been found in list; "
    REGEX_ERROR = " Value didn't match regex in input; "
    OUT_OF_RANGE_ERROR = " Value out of range; "
    NAN_RANGE_ERROR = " Value is not a number; "
    LOWER_UPPER_RANGE_ERROR = " Lower or Upper bound is not defined as an int. check input/input_format.json "

    return_string = ""

    with open(PATH_TO_INPUT_FORMAT_FILE, "r") as input_format:
        if len(fields) != len(headers):
            return SIZE_ERROR 

        input_format = json.loads(input_format.read())

        for field_index in range(0, len(fields)):
            field = fields[field_index]
            header = headers[field_index]


            if input_format[header]["type"] == "list" and frequency_map[header][field] < REPETITION_TO_NORMALIZE:
                domain = input_format[header]["list"]
                if (domain.count(field) == 0):
                    return_string += process_error_string(LIST_ERROR, field, header) 

            if input_format[header]["type"] == "regex":
                regex = input_format[header]["regex"]
                r = re.compile(regex)
                if(r.match(field) == None):
                    return_string += process_error_string(REGEX_ERROR, field, header) 

            if input_format[header]["type"] == "range":
                lower_bound = (input_format[header]["lower_bound"])
                upper_bound = (input_format[header]["upper_bound"])
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

    with open(DATASET_PATH, "r") as dataset_file:

        headers_row = dataset_file.readline()
        headers = process_record(headers_row)
        # NOTE: uso "for i in range(0, len(it)) porque necesito modificar los elementos del iterable"
        # NOTE: en cambio, "for i in it" trata a 'i' como una copia y no como referencia por lo que no es suitable para este caso"
        frequency_map = {}
        for header in headers:
            frequency_map[header] = {}
        
        for line in dataset_file:
            if line == headers_row:
                continue
            fields = process_record(line)
            for header_index in range(0, len(headers)):
                header = headers[header_index]
                if IGNORE_COLUMNS.__contains__(header):
                    continue

                field = fields[header_index]
                if not field in frequency_map[header]:
                    frequency_map[header][field] = 0
                frequency_map[header][field] += 1



    with open(DATASET_PATH, "r") as dataset_file:
        headers_row = dataset_file.readline()
        headers = process_record(headers_row)
        # reset broken_data_file if it has something
        with open(BROKEN_DATA_PATH, "w") as broken_data_file:
            broken_data_file.write("")
        
        
        with open(BROKEN_DATA_PATH, "a") as broken_data_file:
            broken_data_file.write(headers_row.strip() + ",OBSERVACIONES\n")
            for line in dataset_file:
                if line == headers_row:
                    continue
                fields = process_record(line)
                state_of_line = check_state_of_fields(fields,  headers, frequency_map)
                if state_of_line != "Clear":
                    broken_data_file.write(line.strip() + "," + state_of_line + "\n")
    


    distribucion_por_genero = query(DATASET_PATH, "sexo")
    vacunas_por_tipo = query(DATASET_PATH, "vacuna")
    dosis_por_jurisdiccion_residencia = query(DATASET_PATH, "jurisdiccion_residencia", "nombre_dosis_generica")
    dosis_por_jurisdiccion_aplicacion= query(DATASET_PATH, "jurisdiccion_aplicacion", "nombre_dosis_generica")
    dosis_por_edad = query(DATASET_PATH, "grupo_etario", "nombre_dosis_generica")

    print(dosis_por_jurisdiccion_aplicacion) # 2da dosis 
    print(dosis_por_edad) # +60 con refuerzo


    porcentajes_vacunas_por_tipo = {}
    total_de_vacunas = 0
    for fields_str, amount in vacunas_por_tipo.items():
        total_de_vacunas += amount
    for fields_str, amount in vacunas_por_tipo.items():
        porcentajes_vacunas_por_tipo[fields_str] = amount/total_de_vacunas * 100

    segunda_dosis_por_jurisdiccion_aplicacion = {}
    for fields_str, amount in dosis_por_jurisdiccion_aplicacion.items():
        if(fields_str.endswith("2da")):
            segunda_dosis_por_jurisdiccion_aplicacion[fields_str.partition(",")[0]] = amount

    mayores_60_con_refuerzo = 0
    for fields_str, amount in dosis_por_edad.items():
        if(fields_str[0] >= '6' and fields_str[0] != '<' and fields_str.split(",")[-1] == "Refuerzo"):
            mayores_60_con_refuerzo += amount
    with open(OUTPUT_PATH, "w") as output_file:
        pass
    with open(OUTPUT_PATH, "a") as output_file:
        output_file.write(distribucion_por_genero.__str__()+"\n")
        output_file.write(porcentajes_vacunas_por_tipo.__str__()+"\n")
        output_file.write(dosis_por_jurisdiccion_residencia.__str__()+"\n")
        output_file.write(segunda_dosis_por_jurisdiccion_aplicacion.__str__()+"\n")
        output_file.write(mayores_60_con_refuerzo.__str__()+"\n")