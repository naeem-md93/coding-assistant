from typing import List
import torch
import numpy as np
from sentence_transformers import SentenceTransformer


class TransformersEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name).to(device)

    def batch_embed(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts)
        return embeddings
