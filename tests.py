import unittest
from main import * 
# paths to files
PATH_TO_INPUT_FORMAT_FILE="input/input_format.json"
DATASET_PATH= "assets/testDatasets/range_test_dataset.csv"
BROKEN_DATA_PATH = "output/broken_data.csv"
OUTPUT_PATH = "assets/testOutput/test_output.txt"

# misc constants

# amount of repetitions a field value should have to not consider it an error 
# if a field value doesn't appear in its repective list in the input_format.json
REPETITION_TO_NORMALIZE = 30 

# name of the headers that won't appear in the frequency maps
# usually used for unique identifiers in order to not store 
# a ton of crap to memory
IGNORE_COLUMNS= {"id_persona_dw"}

TEST_LIST_DATASET_PATH = "./assets/testDatasets/list_test_dataset.csv"
class TestGetFrequencyMap(unittest.TestCase):
    pass

class TestWriteBrokenData(unittest.TestCase):
    def test_list(self):
        frequency_map = get_frequency_map(TEST_LIST_DATASET_PATH)
        TEST_LIST_OUTPUT="assets/testDatasets/list_test_output.csv"
        with open(OUTPUT_PATH, "w") as output:
            output.write("")
        write_broken_data(TEST_LIST_DATASET_PATH, OUTPUT_PATH, frequency_map)
        with open(TEST_LIST_OUTPUT, "r") as test_output, open(OUTPUT_PATH, "r") as output:
            for test_record in test_output:
                record = output.readline()
                self.assertEqual(test_record, record)

if __name__ == '__main__':
    unittest.main()