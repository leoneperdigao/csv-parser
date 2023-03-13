from collections import defaultdict
from typing import Dict

import numpy as np

from .parser import CsvParser


def compute_statistics(file_path: str) -> Dict[str, Dict[str, float]]:
    """Compute statistics for each numeric column in the given CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary of statistics for each numeric column in the CSV file. The keys of
        the outer dictionary are the column names, and the values are inner dictionaries containing the following keys:
        'min', 'max', 'mean', and 'stdev'.
    """
    csv_parser = CsvParser()
    data = csv_parser.parse(file_path)

    # Collect numeric values for each column
    columns = defaultdict(list)
    for row in data:
        for k, v in row.items():
            if isinstance(v, (int, float)):
                columns[k].append(v)

    # Compute statistics for each column
    stats = {}
    for k, v in columns.items():
        if len(v) == 0:
            stats[k] = {
                'min': None,
                'max': None,
                'mean': None,
                'stdev': None
            }
        else:
            arr = np.array(v)
            stats[k] = {
                'min': np.min(arr),
                'max': np.max(arr),
                'mean': np.mean(arr),
                'stdev': np.std(arr)
            }

    return stats
