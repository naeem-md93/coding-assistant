from typing import Any, Dict, List, Union
import json


def read_json_file(file_path: str) -> Union[Dict, List]:

    with open(file_path, "r") as f:
        data = json.loads(f.read())

    return data