import csv
import os

from csv_parser.parser import CsvParser


def test_parse_csv():
    # set up test data
    data_dir = "data"
    files = os.listdir(data_dir)
    for file in files:
        file_path = os.path.join(data_dir, file)
        with open(file_path, newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')

        # parse the CSV file using the parse_csv() function
        CsvParser.parse(file_path)

        # compare the parsed data with the expected data
