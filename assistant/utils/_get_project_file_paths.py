from typing import List
import os


def get_project_file_paths(project_path: str, include_extensions: List[str], ignore_dirs: List[str]) -> List[str]:

    file_paths = []

    for root, dirs, files in os.walk(project_path, topdown=True):

        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            if ext in include_extensions:
                file_paths.append(file_path)

    return file_paths