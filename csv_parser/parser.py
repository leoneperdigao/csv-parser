import re


def parse_csv(file_path):
    with open(file_path, encoding="utf-8") as f:
        csv_string = f.read()

    lines = re.split(r'\r?\n', csv_string)
    headers = [h.strip('"') for h in re.split(r',', lines[0])]
    data = []
    for line in lines[1:]:
        if line:
            values = re.split(r',', line)
            row = {}
            for i, value in enumerate(values):
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                value = re.sub(r'""', '"', value)
                try:
                    row[headers[i]] = int(value)
                except (ValueError, TypeError):
                    try:
                        row[headers[i]] = float(value)
                    except (ValueError, TypeError):
                        row[headers[i]] = value
            data.append(row)
    return data

