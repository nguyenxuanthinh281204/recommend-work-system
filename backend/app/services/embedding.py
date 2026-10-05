import hashlib
import numpy as np
from typing import List
from app.core.config import settings

def get_deterministic_mock_embedding(text: str, dim: int = 1536) -> List[float]:
    """
    Generates a deterministic 1536-dimensional normalized vector based on bag of words.
    Enables realistic offline semantic similarity testing without requiring an OpenAI API key.
    """
    words = [w.lower().strip() for w in text.split() if len(w) > 1]
    vec = np.zeros(dim, dtype=np.float32)
    
    if not words:
        vec[0] = 1.0
        return vec.tolist()
        
    for word in words:
        # Use md5 to deterministically hash words to vector indices
        h = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if (h % 2 == 0) else -1.0
        vec[idx] += sign
        
        # Add bigram context
        idx2 = (h // dim) % dim
        vec[idx2] += 0.5 * sign

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    else:
        vec[0] = 1.0
    return vec.tolist()

class EmbeddingService:
    def __init__(self):
        self.provider = settings.EMBEDDING_PROVIDER
        self.client = None
        if self.provider == "openai" and settings.OPENAI_API_KEY != "mock-key":
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ").strip()
        if not text:
            text = "empty"

        if self.provider == "openai" and self.client:
            try:
                response = self.client.embeddings.create(
                    input=[text],
                    model=settings.EMBEDDING_MODEL
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"[WARN] OpenAI embedding failed ({e}), falling back to deterministic mock.")
                return get_deterministic_mock_embedding(text, settings.EMBEDDING_DIM)
        
        return get_deterministic_mock_embedding(text, settings.EMBEDDING_DIM)

embedding_service = EmbeddingService()
