from typing import Dict, List, Union
import os
import json


def write_json_file(save_path: str, data: Union[List, Dict]) -> None:

    if os.sep in save_path:
        dir_path, file_name = os.path.split(save_path)
        os.makedirs(dir_path, exist_ok=True)

    with open(save_path, "w") as outfile:
        json.dump(data, outfile, indent=2)