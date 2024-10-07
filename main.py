if __name__ == "__main__":

    path = "assets/testDatasets/modelo_muestra.csv"
    path2 = "output/broken_data.csv"


    print("hello, world")
    with open(path, "r") as file:
     with open(path2, "w") as broken_file_data:

        # leer csv headers
        headers_row = file.readline()
        headers = headers_row.split(",")
        for i in (0, len(headers)-1):
            
            headers[i] = headers[i].strip()
    
        # crear frequency map de los identificadores no unicos  



        # en el frequency map hacer regex para identificar los tipos de vacunas
