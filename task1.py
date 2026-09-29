"""
Backend for the RAG Question-Answering Chatbot.

Run this once to build:
- all_chunks.pkl
- faiss.index

The Streamlit frontend (app.py) loads these files for retrieval.
"""

import os
import pickle
import numpy as np
import faiss
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

CHUNK_SIZE = 500
OVERLAP = 50


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap

    return chunks


print("Loading Mini Wikipedia dataset...")

wiki_dataset = load_dataset(
    "rag-datasets/rag-mini-wikipedia",
    "text-corpus"
)

all_chunks = []

for item in wiki_dataset["passages"]:
    for chunk in chunk_text(item["passage"]):
        all_chunks.append({
            "passage_id": item["id"],
            "chunk": chunk
        })

print(f"Passages: {len(wiki_dataset['passages'])}")
print(f"Chunks: {len(all_chunks)}")

print("Creating embeddings...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

texts = [item["chunk"] for item in all_chunks]

embeddings = embedding_model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)

embeddings = np.asarray(
    embeddings,
    dtype="float32"
)

print("Embedding shape:", embeddings.shape)

print("Building FAISS index...")

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

with open(f"{DATA_FOLDER}/all_chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

faiss.write_index(
    index,
    f"{DATA_FOLDER}/faiss.index"
)

print("Backend setup complete!")
print(f"Saved: {DATA_FOLDER}/all_chunks.pkl")
print(f"Saved: {DATA_FOLDER}/faiss.index")
