import re
import logging
from typing import List, Optional, Set

import nltk
from nltk.corpus import stopwords

from .config import DEBUG

ACTION_WORDS: Set[str] = {
    "use",
    "call",
    "run",
    "create",
    "make",
    "set",
    "get",
    "check",
    "handle",
    "process",
}

_STOP_WORDS_CACHE: Optional[Set[str]] = None


def _get_stop_words() -> Set[str]:
    global _STOP_WORDS_CACHE
    if _STOP_WORDS_CACHE is not None:
        return _STOP_WORDS_CACHE

    try:
        try:
            words = set(stopwords.words("english"))
        except LookupError:
            if DEBUG:
                logging.info("[keywords.py] NLTK stopwords not found, attempting download...")
            nltk.download("stopwords", quiet=True)
            words = set(stopwords.words("english"))

        _STOP_WORDS_CACHE = words | ACTION_WORDS
        if DEBUG:
            logging.debug("[keywords.py] Loaded %d stopwords (including action words)", len(_STOP_WORDS_CACHE))
        return _STOP_WORDS_CACHE
    except Exception as e:
        logging.warning(
            "[keywords.py] Failed to load NLTK stopwords, using minimal fallback set: %s",
            e,
        )
        _STOP_WORDS_CACHE = {
            "the",
            "and",
            "is",
            "in",
            "to",
            "of",
            "a",
            "an",
            "for",
            "on",
            "with",
        } | ACTION_WORDS
        return _STOP_WORDS_CACHE


def is_technical_term(word: str) -> bool:
    return (word[0].isupper() and any(c.islower() for c in word[1:])) or "_" in word or word.isupper()

def is_general_query(query: str) -> bool:
    general_phrases = [
        "what can you do", "what are your capabilities", "help", "who are you",
        "what is this", "tell me about yourself", "capabilities",
        "what do you know", "general questions", "introduce yourself"
    ]
    return any(phrase in query.lower() for phrase in general_phrases)

def extract_keywords(query: str, strict: bool = False) -> List[str]:
    tokens = re.findall(r"[A-Za-z0-9_]+", query)
    if strict:
        keywords = [w for w in tokens if is_technical_term(w)]
    else:
        stop_words = _get_stop_words()
        keywords = []
        for w in tokens:
            if is_technical_term(w):
                keywords.append(w)
            elif w.lower() not in stop_words and len(w) > 2:
                keywords.append(w)
    if DEBUG:
        logging.debug("[keywords.py] Extracted keywords: %s", keywords)
    return keywords
