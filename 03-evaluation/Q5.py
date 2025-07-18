import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline

def cosine(u, v):
    u_norm = np.sqrt(u.dot(u))
    v_norm = np.sqrt(v.dot(v))
    return u.dot(v) / (u_norm * v_norm)

url_prefix = 'https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/03-evaluation/'
results_url = url_prefix + 'rag_evaluation/data/results-gpt4o-mini.csv'
df_results = pd.read_csv(results_url)

pipeline = make_pipeline(
    TfidfVectorizer(min_df=3),
    TruncatedSVD(n_components=128, random_state=1)
)

pipeline.fit(df_results.answer_llm + ' ' + df_results.answer_orig + ' ' + df_results.question)

cosine_similarities = []

for idx, row in df_results.iterrows():
    v_llm = pipeline.transform([row.answer_llm])[0]
    v_orig = pipeline.transform([row.answer_orig])[0]
    cosine_similarities.append(cosine(v_llm, v_orig))

print(np.mean(cosine_similarities))