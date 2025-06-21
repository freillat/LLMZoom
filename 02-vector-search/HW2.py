# from qdrant_client import QdrantClient, models
# client = QdrantClient("http://localhost:6333")

import json
import requests

from fastembed import TextEmbedding
import numpy as np

# Question 1

model = TextEmbedding(model_name="jinaai/jina-embeddings-v2-small-en")
query = 'I just discovered the course. Can I join now?'
embeddings_list = list(model.embed(query))
embeddings = np.array(embeddings_list)
print(f"Embedding size: {embeddings.size}")
min_value = embeddings.min()
print(f"Minimal value in the embedding array: {min_value}")

# Question 2

q = embeddings[0]
doc = 'Can I still join the course after the start date?'
q2 = np.array(list(model.embed(doc)))[0]

print(np.dot(q,q2))

# Question 3

documents = [{'text': "Yes, even if you don't register, you're still eligible to submit the homeworks.\nBe aware, however, that there will be deadlines for turning in the final projects. So don't leave everything for the last minute.",
  'section': 'General course-related questions',
  'question': 'Course - Can I still join the course after the start date?',
  'course': 'data-engineering-zoomcamp'},
 {'text': 'Yes, we will keep all the materials after the course finishes, so you can follow the course at your own pace after it finishes.\nYou can also continue looking at the homeworks and continue preparing for the next cohort. I guess you can also start working on your final capstone project.',
  'section': 'General course-related questions',
  'question': 'Course - Can I follow the course after it finishes?',
  'course': 'data-engineering-zoomcamp'},
 {'text': "The purpose of this document is to capture frequently asked technical questions\nThe exact day and hour of the course will be 15th Jan 2024 at 17h00. The course will start with the first  “Office Hours'' live.1\nSubscribe to course public Google Calendar (it works from Desktop only).\nRegister before the course starts using this link.\nJoin the course Telegram channel with announcements.\nDon’t forget to register in DataTalks.Club's Slack and join the channel.",
  'section': 'General course-related questions',
  'question': 'Course - When will the course start?',
  'course': 'data-engineering-zoomcamp'},
 {'text': 'You can start by installing and setting up all the dependencies and requirements:\nGoogle cloud account\nGoogle Cloud SDK\nPython 3 (installed with Anaconda)\nTerraform\nGit\nLook over the prerequisites and syllabus to see if you are comfortable with these subjects.',
  'section': 'General course-related questions',
  'question': 'Course - What can I do before the course starts?',
  'course': 'data-engineering-zoomcamp'},
 {'text': 'Star the repo! Share it with friends if you find it useful ❣️\nCreate a PR if you see you can improve the text or the structure of the repository.',
  'section': 'General course-related questions',
  'question': 'How can we contribute to the course?',
  'course': 'data-engineering-zoomcamp'}]

V = [ ]
for doc in documents:
    V.append(np.array(list(model.embed(doc['text'])))[0])
V = np.array(V)

print(np.dot(V,q2))

# Question 4

V = [ ]

for doc in documents:
    full_text = doc['question'] + ' ' + doc['text']
    V.append(np.array(list(model.embed(full_text)))[0])
V = np.array(V)

print(np.dot(V,q2))

# Question 5

EMBEDDING_DIMENSIONALITY = 384

for model in TextEmbedding.list_supported_models():
    if model["dim"] == EMBEDDING_DIMENSIONALITY:
        print(json.dumps(model, indent=2))

model = TextEmbedding(model_name="BAAI/bge-small-en")

# Question 6

docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']
    if course_name != 'machine-learning-zoomcamp':
        continue

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

V = [ ]
for doc in documents:
    text = doc['question'] + ' ' + doc['text']
    V.append(np.array(list(model.embed(text)))[0])
V = np.array(V)

# text = doc['question'] + ' ' + doc['text']

query = 'I just discovered the course. Can I join now?'
q = np.array(list(model.embed(query)))[0]

print(np.dot(V,q).max())