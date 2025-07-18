import requests
import pandas as pd
import minsearch

from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from tqdm.auto import tqdm
import numpy as np

url_prefix = 'https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/03-evaluation/'
docs_url = url_prefix + 'search_evaluation/documents-with-ids.json'
documents = requests.get(docs_url).json()

ground_truth_url = url_prefix + 'search_evaluation/ground-truth-data.csv'
df_ground_truth = pd.read_csv(ground_truth_url)
ground_truth = df_ground_truth.to_dict(orient='records')

def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)

def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['document']
        query_text = q['question']
        course_filter = q['course']
        results = search_function(query_text, course_filter)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }

# Initialize Qdrant client (in-memory for this example)
# For a real setup, you'd use QdrantClient(host="localhost", port=6333) or a cloud URL
qdrant_client = QdrantClient(":memory:")

# Initialize FastEmbed model
model_handle = "jinaai/jina-embeddings-v2-small-en"
embedding_model = TextEmbedding(model_name=model_handle)
embedding_size = np.array(list(embedding_model.embed("test"))[0]).shape[0]

# Prepare documents for Qdrant (embedding and payload)
qdrant_points = []
for doc in tqdm(documents, desc="Embedding documents"):
    # Combine question and text as specified
    text_to_embed = doc['question'] + ' ' + doc['text']
    vector = list(embedding_model.embed(text_to_embed))[0].tolist() # Get the embedding, convert to list

    qdrant_points.append(
        models.PointStruct(
            id=int(doc['id'], 16), # Use document ID from the source data
            vector=vector,
            payload=doc # Store the entire document as payload
        )
    )

collection_name = "llm_zoomcamp_docs"
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=embedding_size, distance=models.Distance.COSINE),
)

qdrant_client.upsert(
    collection_name=collection_name,
    wait=True,
    points=qdrant_points
)
print(f"Uploaded {len(qdrant_points)} documents to Qdrant collection '{collection_name}'.")

def qdrant_search(query_text, course_filter):
    query_vector = list(embedding_model.embed(query_text))[0].tolist()
    q_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="course",
                match=models.MatchValue(value=course_filter)
            )
        ]
    )
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=q_filter,
        limit=5
    )
    results = [hit.payload for hit in search_result]
    return results

print(evaluate(ground_truth, qdrant_search))