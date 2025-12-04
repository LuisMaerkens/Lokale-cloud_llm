import logging

import requests

from .config import (
    API_KEY,
    API_TEMPERATURE,
    API_TIMEOUT_SECONDS,
    DEBUG,
    MAX_TOKENS,
    MODEL,
    OLLAMA_API,
)


def query_ollama(prompt: str, max_tokens: int = MAX_TOKENS) -> str:
    """
    Call a (local) Ollama instance via HTTP /api/generate.
    """
    try:
        headers = {
            "Content-Type": "application/json",
        }
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"

        response = requests.post(
            OLLAMA_API,
            headers=headers,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "max_tokens": max_tokens,
                "temperature": API_TEMPERATURE,
            },
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        resp_json = response.json()

        if DEBUG:
            eval_count = resp_json.get("eval_count", 0)
            prompt_eval_count = resp_json.get("prompt_eval_count", 0)
            total_tokens = eval_count + prompt_eval_count
            logging.debug(
                "[api.py] Tokens used: %d (input: %d, output: %d)",
                total_tokens,
                prompt_eval_count,
                eval_count,
            )

        return resp_json.get("response", "")
    except Exception as e:
        logging.error("[api.py] Request to OLLAMA_API failed: %s", e)
        return "[ERROR] Failed to get response from Ollama."