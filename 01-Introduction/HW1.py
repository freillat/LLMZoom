import requests
from elasticsearch import Elasticsearch
import tiktoken

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

print(f"Loaded {len(documents)} documents.")

es_client = Elasticsearch("http://localhost:9200")

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} 
        }
    }
}

index_name = "course-questions"

es_client.indices.create(index=index_name, body=index_settings)
for doc in documents:
    es_client.index(index=index_name, document=doc)

query = "How do execute a command on a Kubernetes pod?"

search_query = {
    "size": 5,
    "query": {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query,
                    "fields": ["question^4", "text"],
                    "type": "best_fields"
                }
            # },
            # "filter": {
            #     "term": {
            #         "course": "data-engineering-zoomcamp"
            #     }
            }
        }
    }
}

response = es_client.search(index=index_name, body=search_query)
top_score = response['hits']['hits'][0]['_score']

print(top_score)

query = "How do copy a file to a Docker container?"

search_query = {
    "size": 3,
    "query": {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query,
                    "fields": ["question^4", "text"],
                    "type": "best_fields"
                }
            },
            "filter": {
                "term": {
                    "course": "machine-learning-zoomcamp"
                }
            }
        }
    }
}

response = es_client.search(index=index_name, body=search_query)

print(response['hits']['hits'][2])

context_template = """
Q: {question}
A: {text}
""".strip()

context = ""   
for hit in response['hits']['hits']:
    doc = hit['_source']
    context = context + f"Q: {doc['question']}\nA: {doc['text']}\n\n"
   
prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()
    
prompt = prompt_template.format(question=query, context=context).strip()

print(len(prompt))

encoding = tiktoken.encoding_for_model("gpt-4o")
tokens = encoding.encode(prompt)
num_tokens = len(tokens)
print(f"Number of tokens: {num_tokens}")