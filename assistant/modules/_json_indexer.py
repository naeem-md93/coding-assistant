from typing import Tuple, Dict, List, Union, Any, Optional
import os

from .. import utils


class JsonIndexer:
    def __init__(self, checkpoint_path: str, file_name: str) -> None:
        self.json_file_path = os.path.join(checkpoint_path, file_name)
        self.content = self.read_file()

    def read_file(self) -> Dict[str, Any]:

        if os.path.exists(self.json_file_path):
            data = utils.read_json_file(self.json_file_path)
            return data

        return {}

    def add_data(self, key: str, data: Any) -> None:
        self.content[key] = data

    def write_content(self) -> None:
        utils.write_json_file(self.json_file_path, self.content)

    def clear_content(self) -> None:
        self.content = {}

    def get_content(self) -> Dict[str, Any]:
        return self.content

    def get_data(self, key: str) -> Any:
        return self.content[key]

    def get_data_or_none(self, key: str) -> Optional[Any]:
        if key in self.content:
            return self.content[key]
        return None

    def remove_data(self, key: str) -> None:
        del self.content[key]

    def is_key_exists(self, key: str) -> bool:
        return key in self.content
