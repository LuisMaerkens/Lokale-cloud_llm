## We Are Frank Doc Assistant

Een kleine command-line chat assistant die vragen beantwoordt over de **We Are Frank Integration Framework** documentatie op basis van lokale JSON-bestanden plus een LLM.

### 1. Vereisten

- Python 3.10 of hoger
- `git` (om de repo te clonen)
- [Ollama](https://ollama.com) geïnstalleerd en draaiend op je machine

### 2. Installatie

In de project-root (waar `main.py` staat):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

Zorg er ook voor dat je een lokaal model hebt gepulld in Ollama, bijvoorbeeld:

```bash
ollama pull llama3.2:3b-instruct
```

### 3. Embedding index bouwen (eenmalig of na doc-update)

De semantic search gebruikt een embedding-index over de JSON-docs in de `data` map.

```bash
python -m src.embeddings
```

Dit maakt o.a. aan:

- `data/embeddings_index.npz`
- `data/embeddings_meta.json`

### 4. Configuratie

In `src/config.py` kun je o.a. instellen:

- LLM / API:
  - `OLLAMA_API` (standaard `http://localhost:11434/api/generate`)
  - `MODEL` (standaard `llama3.2:3b-instruct`, pas aan naar jouw lokale Ollama-model)
  - `API_KEY` (leeg laten als je alleen lokaal draait)
  - `MODEL`
  - `MAX_TOKENS`
  - `API_TIMEOUT_SECONDS`
  - `API_TEMPERATURE`
- Embeddings / search:
  - `EMBEDDING_MODEL_NAME`
  - `EMBEDDING_TOP_K`
  - `MAX_SNIPPETS_PER_FILE`
  - `SNIPPET_CONTEXT_CHARS`
  - `TOP_FILES_LIMIT`
- Chatgedrag:
  - `CONVERSATION_HISTORY_MAXLEN`
  - `MAX_CONTEXT_SNIPPETS`

### 5. Starten

```bash
python main.py
```

Je ziet dan:

- Een welkom-scherm
- Instructies dat je `quit` / `exit` kunt typen om te stoppen
- Optie om `new` / `new chat` te typen voor een nieuwe conversatie

Typ een vraag zoals:

- `how do I use the FxfXmlInputValidator`

De assistant:

1. Haalt relevante document-snippets op (semantic + keyword search).
2. Bouwt een prompt met context + chatgeschiedenis.
3. Vraagt het model om een antwoord (meestal met XML-voorbeelden).


