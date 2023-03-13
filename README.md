# CSV Parser

A Python class that provides methods for parsing CSV files.

## Requirements
The following packages are required to run the code:

* python-dateutil

* You can install these packages by running the following command:

```
pip install -r requirements.txt
```

## Usage

Import the CsvParser class and use the parse method to parse a CSV file:

```python
from csv_parser.parser import CsvParser

csv_parser = CsvParser()
data = csv_parser.parse('path/to/file.csv')
```

The `class` takes several optional arguments:

- `encoding`: The encoding used in the CSV file. Default is `utf-8-sig`.
- `delimiter`: The delimiter used in the CSV file. Default is `,`.
- `quotechar`: The character used to quote fields in the CSV file. Default is `"`.
- `quoting`: The quoting mode used in the CSV file. Default is `False` (no quoting).
- `date_format`: The format used to parse dates in the CSV file. Default is `None`.
- `return_errors`: Whether to return a list of errors or not. Default is `False`.

If `return_errors` is True, a tuple is returned with the list of dictionaries and a list of errors.

If the file cannot be opened or does not exist, an `FileNotFoundError` error will be raised.

## Examples

Parsing a CSV file with default settings:

```python
from csv_parser.parser import CsvParser

csv_parser = CsvParser()
data = CsvParser.parse('data.csv')
```

Parsing a CSV file with a custom delimiter and quoting:

```python
from csv_parser.parser import CsvParser

csv_parser = CsvParser(delimiter=';', quotechar="'", quoting=True)
data = csv_parser.parse('data.csv')
```

Parsing a CSV file with custom date format:

```python
from csv_parser.parser import CsvParser

csv_parser = CsvParser(date_format='%Y-%m-%d %H:%M:%S')
data = csv_parser.parse('data.csv')
```

Parsing a CSV file and returning errors:

```python
from csv_parser.parser import CsvParser

csv_parser = CsvParser(return_errors=True)
data, errors = csv_parser.parse('data.csv')
```

---

# CSV Statistics Calculator

This Python code computes statistics for each numeric column in a given CSV file. The statistics calculated are the minimum value, maximum value, mean and standard deviation.

## Requirements
The following packages are required to run the code:

* numpy
* python-dateutil

* You can install these packages by running the following command:

```
pip install -r requirements.txt
```

## Usage
Import the compute_statistics function from the CsvStatisticsCalculator module and pass the file path of the CSV file as an argument to the function:

```python
from csv_parser.stats import compute_statistics

stats = compute_statistics('path/to/file.csv')
```
The function returns a dictionary of statistics for each numeric column in the CSV file. 
The keys of the outer dictionary are the column names, and the values are inner dictionaries containing the following keys: 'min', 'max', 'mean', and 'stdev'.

## Example
Given the following CSV file:

```txt
Name, Age, Weight
John, 25, 70.5
Jane, 30, 65.2
Bob, 40, 80.0
```
The following code computes the statistics for each numeric column in the file:

```python
from csv_parser.stats import compute_statistics

stats = compute_statistics('data.csv')
print(stats)
```

### Output:

```object
{
    'Age': {'min': 25.0, 'max': 40.0, 'mean': 31.666666666666668, 'stdev': 7.637626260691952},
    'Weight': {'min': 65.2, 'max': 80.0, 'mean': 71.23333333333333, 'stdev': 6.236621979668926}
}
```

## License
This code is licensed under the MIT License.