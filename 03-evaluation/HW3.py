import requests
import pandas as pd
import minsearch

from tqdm.auto import tqdm

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
        results = search_function(query=q['question'], course=q['course'])
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }

def minsearch_search(query, course):
    boost = {'question': 1.5, 'section': 0.1}

    results = index.search(
        query=query,
        filter_dict={'course': course},
        boost_dict=boost,
        num_results=5
    )

    return results

index = minsearch.Index(
    text_fields=["question", "text", "section"],
    keyword_fields=["course", "id"]
)

index.fit(documents)

print(evaluate(ground_truth, minsearch_search))