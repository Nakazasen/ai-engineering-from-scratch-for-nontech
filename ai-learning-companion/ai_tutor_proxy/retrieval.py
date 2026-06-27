"""
Local Lexical Retrieval for the AI Tutor Proxy.
"""
import json
import os
import re

INDEX_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "local_tutor_index.demo.json"
)

def load_index():
    if not os.path.exists(INDEX_PATH):
        return []
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def tokenize(text):
    if not text:
        return []
    text = text.lower()
    # Simple tokenization by word boundaries
    tokens = re.findall(r'\b\w+\b', text)
    # Remove common stopwords (very basic list)
    stopwords = {"là", "gì", "như", "thế", "nào", "có", "không", "của", "và", "trong", "cho", "để", "với"}
    return [t for t in tokens if t not in stopwords]

def retrieve_top_chunks(query: str, top_k: int = 3):
    chunks = load_index()
    if not chunks:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scored_chunks = []
    for chunk in chunks:
        chunk_text = (chunk.get('title', '') + ' ' + chunk.get('heading', '') + ' ' + chunk.get('text', '')).lower()
        score = sum(1 for token in query_tokens if token in chunk_text)
        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Return chunks that have at least a basic match
    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
