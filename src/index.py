import logging
import os
import re
from typing import List

from .config import (
    DATA_DIR,
    DEBUG,
    MAX_SNIPPETS_PER_FILE,
    SNIPPET_CONTEXT_CHARS,
    TOP_FILES_LIMIT,
)

def search_jsonl(keyword: str) -> list:
    keyword = str(keyword)
    file_scores = []

    try:
        for filename in os.listdir(DATA_DIR):
            if not filename.endswith('.json'):
                continue

            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()  
            except Exception as e:
                logging.warning("[index.py] Failed to read file %s: %s", filename, e)
                continue

            pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
            matches = list(pattern.finditer(content))
            score = len(matches)
            if score > 0:
                if DEBUG:
                    logging.debug(
                        "[index.py] Found %d matches in file: %s for keyword '%s'",
                        score, filename, keyword
                    )
                for match in matches[:MAX_SNIPPETS_PER_FILE]:
                    start = max(match.start() - SNIPPET_CONTEXT_CHARS, 0)
                    end = min(match.end() + SNIPPET_CONTEXT_CHARS, len(content))
                    snippet = content[start:end].replace('\n', ' ')
                    file_scores.append((filename, score, snippet))

    except FileNotFoundError as e:
        logging.error("[index.py] DATA_DIR not found: %s", e)
    except Exception as e:
        logging.error("[index.py] Error searching files: %s", e)

    file_scores.sort(key=lambda x: x[1], reverse=True)
    top_files = file_scores[:TOP_FILES_LIMIT]

    results = [{"filename": filename, "excerpt": excerpt} for filename, _, excerpt in top_files]

    if DEBUG:
        distinct_filenames = {filename for filename, _, _ in top_files}
        logging.debug(
            "[index.py] Found %d matching files (distinct), returning %d snippets for keyword '%s'",
            len(distinct_filenames),
            len(results),
            keyword,
        )
        logging.debug("[index.py] Top files: %s", ', '.join(sorted(distinct_filenames)))

    return results

def build_index() -> None:
    """Placeholder for index building."""
    if DEBUG:
        logging.info("[index.py] Building index...")
    pass

if __name__ == "__main__":
    build_index()
