import os
import faiss
import pickle
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

from app.services.file_service import (
    extract_text,
    split_text,
    split_segments_with_timestamps
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

VECTOR_DB_DIR = "vector_db"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


def get_embedding(text: str):
    return embedding_model.encode(text).tolist()


def build_vector_index(file_id: str):
    try:
        data = extract_text(file_id)

        # -----------------------
        # Error handling
        # -----------------------
        if not data:
            return {"error": "No content"}

        if isinstance(data, str):
            if data.startswith("Error") \
               or data == "File not found" \
               or data == "Unsupported file type":
                return {"error": data}

        chunks = []
        metadata = []

        # -----------------------
        # PDF / TXT
        # -----------------------
        if isinstance(data, str):
            text_chunks = split_text(data)

            for chunk in text_chunks:
                chunks.append(chunk)
                metadata.append({
                    "text": chunk,
                    "timestamp": None
                })

        # -----------------------
        # Audio / Video
        # -----------------------
        elif isinstance(data, list):
            segment_chunks = split_segments_with_timestamps(data)

            for item in segment_chunks:
                chunks.append(item["text"])
                metadata.append(item)

        if not chunks:
            return {
                "error": "No chunks created"
            }

        # -----------------------
        # Embeddings
        # -----------------------
        vectors = np.array(
            [get_embedding(c) for c in chunks]
        ).astype("float32")

        dimension = vectors.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(vectors)

        # -----------------------
        # Save
        # -----------------------
        index_path = os.path.join(
            VECTOR_DB_DIR,
            f"{file_id}.index"
        )

        meta_path = os.path.join(
            VECTOR_DB_DIR,
            f"{file_id}.pkl"
        )

        faiss.write_index(
            index,
            index_path
        )

        with open(meta_path, "wb") as f:
            pickle.dump(metadata, f)

        print("✅ Index created:", file_id)

        return {
            "message":
            "Vector index created"
        }

    except Exception as e:
        print("❌ Index error:", e)
        return {
            "error": str(e)
        }


def get_relevant_chunks(file_id: str, query: str, top_k: int = 3):
    try:
        index_path = os.path.join(
            VECTOR_DB_DIR,
            f"{file_id}.index"
        )

        meta_path = os.path.join(
            VECTOR_DB_DIR,
            f"{file_id}.pkl"
        )

        if not os.path.exists(index_path) or not os.path.exists(meta_path):
            return []

        index = faiss.read_index(index_path)

        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)

        query_vector = np.array(
            [get_embedding(query)]
        ).astype("float32")

        distances, indices = index.search(query_vector, top_k)

        results = []

        for pos, i in enumerate(indices[0]):
            if i < len(metadata):
                distance = distances[0][pos]

                # keep relevant matches only
                if distance < 2.5:
                    results.append(metadata[i])

        return results

    except Exception as e:
        print("Search error:", e)
        return []