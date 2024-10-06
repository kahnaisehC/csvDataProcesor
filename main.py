if __name__ == "__main__":

    path = "assets/testDatasets/modelo_muestra.csv"
    path2 = "output/broken_data.csv"


    print("hello, world")
    file = open(path, "r")
    # print(file.readline())
    fil2 = open(path2, "w")
    fil2.write(file.readline())





    file.close()