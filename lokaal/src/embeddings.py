import json
import logging
import os
from typing import Any, Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from .config import (
    DATA_DIR,
    DEBUG,
    EMBEDDING_INDEX_PATH,
    EMBEDDING_META_PATH,
    EMBEDDING_MODEL_NAME,
    EMBEDDING_TOP_K,
)

_model: SentenceTransformer | None = None
_embeddings: np.ndarray | None = None
_meta: List[Dict[str, Any]] | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        if DEBUG:
            logging.debug("[embeddings.py] Loading embedding model: %s", EMBEDDING_MODEL_NAME)
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def _load_index() -> Tuple[np.ndarray, List[Dict[str, Any]]]:
    global _embeddings, _meta
    if _embeddings is not None and _meta is not None:
        return _embeddings, _meta

    if not os.path.exists(EMBEDDING_INDEX_PATH) or not os.path.exists(EMBEDDING_META_PATH):
        raise FileNotFoundError("Embedding index or metadata not found. Run build_embedding_index() first.")

    if DEBUG:
        logging.debug("[embeddings.py] Loading embeddings from %s", EMBEDDING_INDEX_PATH)
    data = np.load(EMBEDDING_INDEX_PATH)
    _embeddings = data["embeddings"]

    with open(EMBEDDING_META_PATH, "r", encoding="utf-8") as f:
        _meta = json.load(f)

    return _embeddings, _meta  # type: ignore[return-value]


def build_embedding_index() -> None:
    model = _get_model()

    texts: List[str] = []
    meta: List[Dict[str, Any]] = []

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logging.warning("[embeddings.py] Failed to read file %s: %s", filename, e)
            continue

        texts.append(content)
        meta.append({"filename": filename})

    if not texts:
        logging.warning("[embeddings.py] No documentation files found to index.")
        return

    if DEBUG:
        logging.debug("[embeddings.py] Encoding %d documents for embeddings index", len(texts))

    embeddings = model.encode(texts, batch_size=32, show_progress_bar=DEBUG, convert_to_numpy=True)

    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    embeddings = embeddings / norms

    os.makedirs(os.path.dirname(EMBEDDING_INDEX_PATH), exist_ok=True)
    np.savez_compressed(EMBEDDING_INDEX_PATH, embeddings=embeddings)

    with open(EMBEDDING_META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f)

    logging.info("[embeddings.py] Built embeddings index for %d documents", len(texts))


def semantic_search(query: str, top_k: int = EMBEDDING_TOP_K) -> List[Dict[str, str]]:
    embeddings, meta = _load_index()
    model = _get_model()

    query_vec = model.encode([query], convert_to_numpy=True)[0]
    # Normalize
    norm = np.linalg.norm(query_vec)
    if norm == 0:
        norm = 1.0
    query_vec = query_vec / norm

    # Cosine similarity via dot product
    scores = embeddings @ query_vec
    top_k = min(top_k, len(scores))
    if top_k <= 0:
        return []

    top_indices = np.argsort(-scores)[:top_k]

    results: List[Dict[str, str]] = []
    for idx in top_indices:
        info = meta[int(idx)]
        filename = info["filename"]
        results.append(
            {
                "filename": filename,
                "excerpt": "",
            }
        )

    if DEBUG:
        logging.debug("[embeddings.py] Semantic search returned %d results for query '%s'", len(results), query)

    return results


if __name__ == "__main__":
    build_embedding_index()


