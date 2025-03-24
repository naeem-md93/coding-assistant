from typing import Tuple, Dict, List, Union, Any
import os
import copy
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

from .. import utils


class JsonIndexer:
    def __init__(self, checkpoint_path: str, file_name: str) -> None:
        self.json_file_path = os.path.join(checkpoint_path, file_name)
        self.content = self.read_file()

    @staticmethod
    def process_data_after_reading(data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:

        result = {}
        for k, v in data.items():
            result[k] = copy.deepcopy(v)
            result[k]["content_embedding"] = np.array(result[k]["content_embedding"], dtype=np.float32)
            result[k]["description_embedding"] = np.array(result[k]["description_embedding"], dtype=np.float32)

        return result

    @staticmethod
    def process_data_before_writing(data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:

        result = {}
        for k, v in data.items():
            result[k] = copy.deepcopy(v)
            result[k]["content_embedding"] = result[k]["content_embedding"].tolist()
            result[k]["description_embedding"] = result[k]["description_embedding"].tolist()

        return result

    def read_file(self) -> Dict[str, Dict[str, Any]]:

        if os.path.exists(self.json_file_path):
            data = utils.read_json_file(self.json_file_path)
            data = self.process_data_after_reading(data)
            return data

        return {}

    def update_content(self, fp: str, data: Dict[str, Union[str, np.ndarray]]) -> None:
        self.content[fp] = data

    def write_content(self) -> None:

        data = self.process_data_before_writing(self.content)
        utils.write_json_file(self.json_file_path, data)

    def clear_content(self) -> None:
        self.content = {}

    def get_content(self) -> Dict[str, Dict[str, Any]]:
        return self.content

    def get_data(self, fp: str) -> Dict[str, Any]:
        if fp in self.get_content():
            return self.get_content()[fp]
        return {}

    def remove_data(self, fp: str) -> None:
        del self.content[fp]

    def is_in_content(self, fp: str) -> bool:
        return fp in self.content


    def search_content(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:

        file_paths = []
        embeddings = []
        results = []

        query_embedding = np.reshape(query_embedding, (1, -1))

        for v in self.get_content().values():
            file_paths.append(v["file_path"])
            embeddings.append(v["description_embedding"])

        embeddings = np.row_stack(embeddings)
        distances = euclidean_distances(query_embedding, embeddings)

        distances = distances[0]

        lowest_indices = np.argsort(distances)[:top_k]

        for i in lowest_indices:
            results.append(self.get_data(file_paths[i]))

        return results