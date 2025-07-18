import numpy as np
import pandas as pd

from rouge import Rouge
from tqdm.auto import tqdm

def cosine(u, v):
    u_norm = np.sqrt(u.dot(u))
    v_norm = np.sqrt(v.dot(v))
    return u.dot(v) / (u_norm * v_norm)

url_prefix = 'https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/03-evaluation/'
results_url = url_prefix + 'rag_evaluation/data/results-gpt4o-mini.csv'
df_results = pd.read_csv(results_url)

rouge_scorer = Rouge()
F1_scores = []

for idx, row in tqdm(df_results.iterrows(), total=len(df_results), desc="Processing"):
    scores = rouge_scorer.get_scores(row.answer_llm, row.answer_orig)[0]
    F1_scores.append(scores['rouge-1']['f'])

print(np.mean(F1_scores))