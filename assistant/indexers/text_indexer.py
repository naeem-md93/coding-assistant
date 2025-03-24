import os

from .. import utils


class TextIndexer:
    def __init__(self, checkpoint_path: str, file_name: str) -> None:
        self.text_file_path = os.path.join(checkpoint_path, file_name)
        self.content = self.read_file()

    def read_file(self) -> str:
        if os.path.exists(self.text_file_path):
            return utils.read_text_file(self.text_file_path)
        return ""

    def update_content(self, text) -> None:
        self.content = text

    def append_content(self, text: str, separator: str) -> None:
        self.content += separator
        self.content += text

    def write_content(self) -> None:
        utils.write_text_file(self.text_file_path, self.content)

    def clear_content(self) -> None:
        self.content = ""

    def get_content(self) -> str:
        return self.content
