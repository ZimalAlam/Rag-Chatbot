# file: embedder.py

import os
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks(chunk_folder: str):
    """Load all chunk texts and metadata."""
    chunk_path = Path(chunk_folder)
    texts = []
    metadata = []

    for pdf_folder in chunk_path.iterdir():
        if pdf_folder.is_dir():
            for chunk_file in sorted(pdf_folder.glob("*.txt")):
                with open(chunk_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()

                if not text:
                    continue

                texts.append(text)
                metadata.append({
                    "pdf": pdf_folder.name,
                    "chunk_file": chunk_file.name,
                    "text": text
                })

    return texts, metadata


def build_faiss_index(texts, model):
    """Convert texts to embeddings and store in FAISS."""
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index


def save_index(index, metadata, save_folder: str):
    """Save FAISS index and metadata."""
    save_path = Path(save_folder)
    save_path.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(save_path / "faiss.index"))

    with open(save_path / "metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print(f"Saved FAISS index with {len(metadata)} vectors.")


# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    chunked_folder = "chunked_texts"
    index_folder = "faiss_index"

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    texts, metadata = load_chunks(chunked_folder)

    print(f"Loaded {len(texts)} chunks.")
    index = build_faiss_index(texts, model)

    save_index(index, metadata, index_folder)
    print("Embedding pipeline complete!")
