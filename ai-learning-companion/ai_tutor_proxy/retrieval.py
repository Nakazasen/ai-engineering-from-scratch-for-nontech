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
            data = json.load(f)
            if isinstance(data, dict):
                chunks = data.get("chunks", [])
                if isinstance(chunks, list):
                    return chunks
                return []
            elif isinstance(data, list):
                return data
            return []
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
        if not isinstance(chunk, dict):
            continue
            
        title = chunk.get('title', '')
        heading = chunk.get('heading', '')
        text = chunk.get('text', '')
        
        chunk_text = (str(title) + ' ' + str(heading) + ' ' + str(text)).lower()
        score = sum(1 for token in query_tokens if token in chunk_text)
        if score > 0:
            safe_chunk = {
                "chunk_id": chunk.get("chunk_id"),
                "lesson_id": chunk.get("lesson_id"),
                "title": title,
                "heading": heading,
                "text": text,
                "source_doc_path": chunk.get("source_doc_path") or chunk.get("source_path"),
                "source_type": chunk.get("source_type"),
                "score": float(score)
            }
            scored_chunks.append((score, safe_chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Return chunks that have at least a basic match
    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
