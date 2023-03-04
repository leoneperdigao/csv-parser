import datetime
from dateutil.parser import parse as parse_date


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        try:
            int(value, 16)  # Check for hexadecimal integers
            return True
        except ValueError:
            try:
                int(value, 2)  # Check for binary integers
                return True
            except ValueError:
                return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        try:
            float(value.replace(",", "."))  # Replace comma with dot as decimal separator
            return True
        except ValueError:
            return False


def is_date(value, date_format=None):
    try:
        if date_format:
            datetime.datetime.strptime(value, date_format)
        else:
            parse_date(value)
        return True
    except ValueError:
        return False


def parse_csv(file_path, delimiter=',', quotechar='"', quoting=0, date_format=None):
    with open(file_path, encoding="utf-8-sig") as f:
        lines = f.readlines()

    headers = [h.strip(quotechar) for h in lines[0].strip().split(delimiter)]
    data = []
    for i, line in enumerate(lines[1:]):
        if line.strip():
            if quoting == 0:
                values = line.strip().split(delimiter)
            else:
                values = line.strip().split(delimiter + quotechar)
                values = [v.strip(quotechar) for v in values]
            if len(values) != len(headers):
                error = f"Line {i+2} has {len(values)} values, expected {len(headers)}"
                data.append({"Error": error})
                continue
            row = {}
            for j, value in enumerate(values):
                if value.startswith(quotechar) and value.endswith(quotechar):
                    value = value[1:-1]
                    value = value.replace(quotechar*2, quotechar)
                if is_int(value):
                    row[headers[j]] = int(value)
                elif is_float(value):
                    row[headers[j]] = float(value)
                elif date_format and is_date(value, date_format):
                    row[headers[j]] = datetime.datetime.strptime(value, date_format)
                elif is_date(value):
                    row[headers[j]] = parse_date(value)
                else:
                    row[headers[j]] = value
            data.append(row)
    return data