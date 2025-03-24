from typing import List, Union
import torch
import numpy as np
from sentence_transformers import SentenceTransformer


class SimpleEmbedder:
    """
    Handles embedding generation using a pre-trained transformer model.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the Embedding module.
        """
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # Keep device
        self.model = self.model.to(self.device)

        print(f"Embedder loaded: {model_name}")

    def embed(self, text: str) -> np.ndarray:
        """
        Generates embeddings for a given text.

        Args:
            text: The text to embed.

        Returns:
            A numpy array representing the embedding.
        """
        embeddings = self.model.encode(text)
        return embeddings

    def batch_embed(self, texts: List[str]) -> np.ndarray:
        """
        Generates embeddings for a list of texts.

        Args:
            texts: List of texts to embed.

        Returns:
            A numpy array representing the embeddings.
        """
        embeddings = self.model.encode(texts)
        return embeddings
