import os

# ---------- PATHS ----------
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# ---------- LLM / API SETTINGS ----------
OLLAMA_API = "https://ollama.com/api/generate"
API_KEY = "YOUR_API_KEY"
MODEL = "gpt-oss:120b"
MAX_TOKENS = 200
API_TIMEOUT_SECONDS = 120
API_TEMPERATURE = 0.1

# ---------- EMBEDDINGS / SEMANTIC SEARCH ----------
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_index.npz")
EMBEDDING_META_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_meta.json")
EMBEDDING_TOP_K = 50

# ---------- CHAT / PROMPT SETTINGS ----------
CONVERSATION_HISTORY_MAXLEN = 10
STRUCTURE_INSTRUCTION = (
    "Structure your response as alternating text and code blocks, like: text, ```code```, "
    "text. Do not use numbered lists, labels, or bullet points. Keep answers very concise."
)
MAX_CONTEXT_SNIPPETS = 12

# ---------- INDEX / SEARCH SETTINGS ----------
MAX_LINES_PER_CHUNK = 50
MAX_SNIPPETS_PER_FILE = 3
SNIPPET_CONTEXT_CHARS = 100
TOP_FILES_LIMIT = 40

# ---------- GENERAL APP SETTINGS ----------
DEBUG = True
# ----------------------------
