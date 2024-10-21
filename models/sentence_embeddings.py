from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class SentenceEmbeddings:
    def __init__(self, model_path: str = 'sentence-transformers/paraphrase-MiniLM-L6-v2'):
        self.model_path = model_path
        self.model = SentenceTransformer(model_path)

    def encode(self, sentences: List[str]) -> np.ndarray:
        return self.model.encode(sentences)
