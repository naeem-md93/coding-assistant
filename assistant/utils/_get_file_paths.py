from typing import List
import os


def get_file_paths(path: str, extensions: List[str], exclude_dirs: List[str]) -> List[str]:

    file_paths = []
    for root, _, files in os.walk(path):

        if sum([(x in root) for x in exclude_dirs]) == 0:
            for file in files:
                if os.path.splitext(file)[1] in extensions:
                    file_paths.append(os.path.join(root, file))

    return file_paths
