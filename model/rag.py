from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import numpy as np

# Load dataset
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(base_dir, 'dataset', 'dataset.json')

with open(dataset_path, "r") as f:
    documents = json.load(f)

corpus = [doc['instruction'] for doc in documents]

# --- OPTIMIZATION START ---
# Using TF-IDF instead of BERT/Transformers to save RAM.
# This runs on CPU and uses < 100MB RAM.
print("Vectorizing database (TF-IDF)...")
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(corpus)
# --- OPTIMIZATION END ---

def retrieve_response(user_query):
    # Transform user query into the same vector space
    query_vec = vectorizer.transform([user_query])
    
    # Calculate similarity
    cosine_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Find best match
    best_match_index = np.argmax(cosine_scores)
    best_score = cosine_scores[best_match_index]
    
    print(f"Best score: {best_score}")

    # Threshold adjustment: TF-IDF scores are often lower than Embeddings.
    # 0.2 is a reasonable starting point for keyword overlap.
    if best_score < 0.2: 
        # Keeping your custom error message
        return "I'm not sure I understand. Could you rephrase that?", "Uncertain"
    
    return documents[best_match_index]['response'], documents[best_match_index]['category']