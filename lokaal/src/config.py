import os

# ---------- PATHS ----------
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# ---------- LLM / API SETTINGS (OLLAMA LOCAL) ----------
OLLAMA_API = "http://localhost:11434/api/generate"
API_KEY = ""  # leeg laten voor lokale Ollama
MODEL = "llama3.2:3b-instruct"  # gebruik een iets groter, maar nog steeds snel model
MAX_TOKENS = 200      # max nieuw te genereren tokens
API_TEMPERATURE = 0.2 # iets meer variatie, nog steeds redelijk feitelijk
API_TIMEOUT_SECONDS = 1200

# ---------- EMBEDDINGS / SEMANTIC SEARCH ----------
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_index.npz")
EMBEDDING_META_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_meta.json")
EMBEDDING_TOP_K = 50

# ---------- CHAT / PROMPT SETTINGS ----------
CONVERSATION_HISTORY_MAXLEN = 10
STRUCTURE_INSTRUCTION = (
    "Answer clearly and concisely. Prefer XML examples where they help the explanation. "
    "You may use short bullet points and code blocks, but avoid long essays."
)
MAX_CONTEXT_SNIPPETS = 8

# ---------- INDEX / SEARCH SETTINGS ----------
MAX_LINES_PER_CHUNK = 50
MAX_SNIPPETS_PER_FILE = 2
SNIPPET_CONTEXT_CHARS = 300
TOP_FILES_LIMIT = 40

# ---------- GENERAL APP SETTINGS ----------
DEBUG = True
# ----------------------------
