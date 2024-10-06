if __name__ == "__main__":

    path = "assets/datasets/datos_nomivac_parte2.csv"
    # path = "assets/testDatasets/modelo_muestra.csv"
    path2 = "output/broken_data.csv"

    with open(path, "r") as file, open(path2, "w") as file2:
        amount_masc_vacc = 0
        amount_fem_vacc = 0
        headers = file.readline().split(",")
        map_of_set_of_values = [{x} for x in headers]

        for line in file:
            line = line.rstrip().split(sep=",")
            for i in range (0, len(headers)):
                if headers[i] == "id_persona_dw\n":
                    continue
                if headers[i] == "sexo":
                    amount_fem_vacc += line[i] == "F"
                    amount_masc_vacc += line[i] == "M"

                map_of_set_of_values[i].add(line[i])

        for header in map_of_set_of_values:
            print()
            for item in header:
                
                print(item, end=", ")


        print("amount of males: ", amount_masc_vacc)
        print("amount of females: ", amount_fem_vacc)
    




