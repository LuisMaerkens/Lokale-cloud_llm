import logging
from typing import List

from .api import query_ollama
from .embeddings import semantic_search
from .index import search_jsonl
from .keywords import extract_keywords, is_general_query
from .prompt import build_prompt_with_context, conversation_history

def chat(user_input: str) -> str:
    logging.debug("[chat.py] User input: '%s'", user_input)

    is_general = is_general_query(user_input)
    if is_general:
        relevant_lines: List[str] = []
    else:
        relevant_lines: List[str] = []

        try:
            semantic_results = semantic_search(user_input)
        except Exception as e:
            logging.warning("[chat.py] Semantic search failed, falling back to keyword search: %s", e)
            semantic_results = []

        semantic_filenames = {r["filename"] for r in semantic_results}

        keywords = extract_keywords(user_input)
        for keyword in keywords:
            lines = search_jsonl(keyword)
            for line in lines:
                filename = line["filename"]
                prefix = "[SEMANTIC HIT] " if filename in semantic_filenames else ""
                relevant_lines.append(
                    f"{prefix}File: {filename}\nSnippet: {line['excerpt']}"
                )

    prompt = build_prompt_with_context(user_input, relevant_lines, is_general=is_general)
    response = query_ollama(prompt)

    conversation_history.append({"role": "User", "content": user_input})
    conversation_history.append({"role": "Assistant", "content": response})
    return response.strip()
