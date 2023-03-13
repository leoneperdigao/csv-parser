import datetime
import logging
import re

from dateutil.parser import parse as parse_date, ParserError


class CsvParser:
    """
    A class that provides methods for parsing CSV files.

    Args:
        encoding (str): The encoding used in the CSV file. Default is 'utf-8-sig'.
        delimiter (str): The delimiter used in the CSV file. Default is ','.
        quotechar (str): The character used to quote fields in the CSV file. Default is '"'.
        quoting (bool): The quoting mode used in the CSV file. Default is False (no quoting).
        date_format (str): The format used to parse dates in the CSV file. Default is None.
        return_errors (bool): Whether to return a list of errors or not. Default is False.
    """

    # Configure logger
    __logger = logging.getLogger(__name__)
    __logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    __logger.addHandler(ch)

    def __init__(self, encoding="utf-8-sig", delimiter=',', quotechar='"', quoting=False, date_format=None, return_errors=False):
        self.__encoding = encoding
        self.__delimiter = delimiter
        self.__quotechar = quotechar
        self.__quoting = quoting
        self.__date_format = date_format
        self.__return_errors = return_errors

    @staticmethod
    def __is_int(value):
        """
        Returns True if the value can be converted to an integer, False otherwise.
        """
        if not value:
            return False
        regex = r"^[-+]?\d+$"
        return bool(re.match(regex, value))

    @staticmethod
    def __is_float(value):
        """
        Returns True if the value can be converted to a float, False otherwise.
        """
        try:
            float(value)
            return True
        except ValueError:
            try:
                float(value.replace(",", "."))  # Replace comma with dot as decimal separator
                return True
            except ValueError:
                return False

    @staticmethod
    def __is_date(value, date_format=None):
        """
        Returns True if the value can be converted to a datetime object, False otherwise.
        """
        try:
            if date_format:
                datetime.datetime.strptime(value, date_format)
            else:
                parse_date(value)
            return True
        except (ValueError, ParserError, OverflowError):
            return False

    @staticmethod
    def __read_file(file_path, encoding):
        try:
            with open(file_path, mode="r", encoding=encoding) as f:
                lines = f.readlines()
        except FileNotFoundError:
            CsvParser.__logger.fatal(f'Aborted! Could not open file: {file_path}.')
            raise
        return lines

    def parse(self, file_path):
        """
        Parses a CSV file and returns the data as a list of dictionaries.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            A list of dictionaries, where each dictionary represents a row in the CSV file.
            If `return_errors` is True, a tuple is returned with the list of dictionaries and a list of errors.
            If the file cannot be opened or is empty, an empty list is returned.
        """
        lines = CsvParser.__read_file(file_path, self.__encoding)

        headers = [h.strip(self.__quotechar) for h in lines[0].strip().split(self.__delimiter)]
        data = []
        errors = []
        for i, line in enumerate(lines[1:]):
            if line.strip():
                if not self.__quoting:
                    values = line.strip().split(self.__delimiter)
                else:
                    values = line.strip().split(self.__delimiter + self.__quotechar)
                    values = [v.strip(self.__quotechar) for v in values]
                if len(values) != len(headers):
                    error_detail = {
                        "line": i + 2,
                        "message": f"Line {i + 2} has {len(values)} values, expected {len(headers)}."
                    }
                    errors.append(error_detail)
                    CsvParser.__logger.warning(error_detail['message'])
                    continue
                row = {}
                for j, value in enumerate(values):
                    if value.startswith(self.__quotechar) and value.endswith(self.__quotechar):
                        value = value[1:-1]
                        value = value.replace(self.__quotechar * 2, self.__quotechar)
                    if CsvParser.__is_int(value):
                        row[headers[j]] = int(value)
                    elif CsvParser.__is_float(value):
                        row[headers[j]] = float(value)
                    elif self.__date_format and CsvParser.__is_date(value, self.__date_format):
                        row[headers[j]] = datetime.datetime.strptime(value, self.__date_format)
                    elif CsvParser.__is_date(value, self.__date_format):
                        row[headers[j]] = parse_date(value)
                    else:
                        row[headers[j]] = value
                data.append(row)

        if self.__return_errors:
            return data, errors

        if len(errors):
            CsvParser.__logger.warning("File partially parsed. One or more entries contain errors.")

        return data
