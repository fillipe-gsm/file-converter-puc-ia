from pathlib import Path
from typing import Dict, List, Optional, Union


def csv2json(file_path: str, separator: str = ","):
    """"""

    if Path(file_path).is_file():
        file_names = [file_path]

    json_lists = [
        _csv2json_file(file_name, separator=separator)
        for file_name in file_names
    ]



def csv2json_file(file_name: str, separator: str = ",") -> List[Dict[str, str]]:
    """Converts file(s) from CSV format to JSON"""

    def _process_line(
        line: str
    ) -> Dict[str, Optional[Union[int, float, str]]]:
        """"""
        line_values = line.strip().split(separator)
        d_json = {}
        for key, value in zip(keys, line_values):
            d_json[key] = _parse_value(value)

        return d_json

    with open(file_name, "r") as f:
        header = next(f)
        keys = header.strip().split(separator)
        json_list = [_process_line(line) for line in f]

    return json_list


def _parse_value(value: str) -> Optional[Union[int, float, str]]:
    """Parse an incoming value into a number, string or None
    Here are the possibilities:
        - An empty string: set to None to be converted to a null later;
        - All digits: convert into an integer;
        - Digits and a decimal point: convert into a float;
        - Otherwise, return the original string.
    """
    if not value:
        return None

    if value.isdigit():
        return int(value)

    # Finally, we are left with a floating point or a regular string
    try:
        return float(value)
    except ValueError:
        return value
