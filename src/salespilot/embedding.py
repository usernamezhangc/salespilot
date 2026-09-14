from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("BAAI/bge-base-zh-v1.5", cache_folder="models")

def embed_text(text: str) -> list[float]:
    vector = _model.encode(text, normalize_embeddings=True)
    return vector.tolist()