# from qdrant_client import QdrantClient, models
# client = QdrantClient("http://localhost:6333")

# import requests

from fastembed import TextEmbedding
import numpy as np

model = TextEmbedding(model_name="jinaai/jina-embeddings-v2-small-en")
query = 'I just discovered the course. Can I join now?'
embeddings_list = list(model.embed(query))
embeddings = np.array(embeddings_list)
print(f"Embedding size: {embeddings.size}")
min_value = embeddings.min()
print(f"Minimal value in the embedding array: {min_value}")