from collections import deque
from typing import List

from .config import (
    CONVERSATION_HISTORY_MAXLEN,
    MAX_CONTEXT_SNIPPETS,
    MAX_TOKENS,
    STRUCTURE_INSTRUCTION,
)
from .keywords import extract_keywords
from .utils import rank_relevant_lines

conversation_history = deque(maxlen=CONVERSATION_HISTORY_MAXLEN)

def build_prompt_with_context(query: str, relevant_lines: List[str], is_general: bool = False) -> str:
    chat_context = "\n".join(f"{msg['role']}: {msg['content']}" for msg in conversation_history)
    if relevant_lines:
        ranked = rank_relevant_lines(relevant_lines, extract_keywords(query))
        context_snippets = "\n".join(ranked[:MAX_CONTEXT_SNIPPETS])
        prompt = f"""
You are an expert assistant specialized in the We Are Frank Integration Framework.
Only use the provided documentation to answer the user's questions.
If you don't know the answer, respond with "I don't know".
You almost always answer with xml code snippets never another code language.
The documentation snippets may be partial; clearly mention any missing pieces and answer as far as the snippets allow.
Do not provide unrelated information. {STRUCTURE_INSTRUCTION}

Documentation:
{context_snippets}

Conversation History:
{chat_context}

User Question: {query}
Assistant:"""
    elif is_general:
        prompt = f"""
You are an expert assistant specialized in the We Are Frank Integration Framework.
You can answer general questions about yourself and your capabilities.
The documentation snippets may be partial; clearly mention any missing pieces and answer as far as the snippets allow.
{STRUCTURE_INSTRUCTION}

Conversation History:
{chat_context}

User Question: {query}
Assistant:"""
    else:
        prompt = f"""
You are an expert assistant specialized in the We Are Frank Integration Framework.
Only answer questions using WAF Integration Framework documentation.
If you don't know the answer, respond with "I don't know".
The documentation snippets may be partial; clearly mention any missing pieces and answer as far as the snippets allow.
{STRUCTURE_INSTRUCTION}

Conversation History:
{chat_context}

User Question: {query}
Assistant:"""
    return prompt
