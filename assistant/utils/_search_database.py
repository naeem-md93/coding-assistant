from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances


def search_database(query_embedding: np.ndarray, indexer_data: Dict[str, Any], topk: int) -> List[Dict[str, Any]]:

    file_paths = [d["path"] for d in indexer_data.values()]
    embeddings = np.vstack([d["embedding"] for d in indexer_data.values()])
    results = []

    distances = euclidean_distances(query_embedding, embeddings)

    distances = distances[0]

    lowest_indices = np.argsort(distances)[:topk]

    for i in lowest_indices:
        results.append(indexer_data[file_paths[i]])

    return results