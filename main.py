import string

if __name__ == "__main__":
    columns_to_ignore = {"id_persona_dw"}
    path = "assets/testDatasets/modelo_muestra.csv"
    path2 = "output/broken_data.csv"


    print("hello, world")
    with open(path, "r") as file, open(path2, "w") as broken_file_data:

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
            print(line)
            for field_index in range(0, len(fields)):
                fields[field_index] = fields[field_index].strip()
            for header_index in range(0, len(headers)):
                # obtener header e ignorar si esta dentro del set de identificadores unicos
                header = headers[header_index]
                if columns_to_ignore.__contains__(header):
                    continue

                # si len(fields) > len(headers) guardar line en output/large_data + OBSERVACIONES
                if len(fields) > len(headers):
                    # TODO: anadir anadir row to large_data y crear large_data
                    continue
                # si len(fields) < len(headers) guardar line en output/short_data + OBSERVACIONES
                if len(fields) < len(headers):
                    # TODO: anadir row a short_data
                    continue
                # si len(fields) == len(headers) proceder
                field = fields[header_index]
                if not field in frequency_map[header]:
                    frequency_map[header][field] = 0
                frequency_map[header][field] += 1

        print(frequency_map)
                

            


           
        

        # en el frequency map hacer regex para identificar los tipos de vacunas
