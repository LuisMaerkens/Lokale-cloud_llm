
### 1. Vereisten

- Python 3.10 of hoger
- `git` (om de repo te clonen)

### 2. Installatie

In de project-root (waar `main.py` staat):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```


### 3. Configuratie

In `src/config.py` kun je o.a. instellen:

- LLM / API:
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


**Vergeet niet:** Ga naar de ollama website en maak een gratis account aan 
en geneer een api key vergeet die niet toe te voegen aan de config file.

### 4. Starten

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


