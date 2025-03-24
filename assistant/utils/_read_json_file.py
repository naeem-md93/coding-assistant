from typing import Any, Dict, List, Union
import json


def read_json_file(path: str) -> Union[Dict[str, Any], List[str]]:
    with open(path, "r") as f:
        data = json.loads(f.read())
    return data