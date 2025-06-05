import os

from .. import utils


class FileManager:
    def __init__(self, file_path: str) -> None:
        self.path = file_path
        self.name = os.path.basename(file_path)
        self.ext = os.path.splitext(self.name)[1].lower()
        self.content = utils.read_text_file(self.path)
        self.hash = utils.hash_file_content(self.content)
