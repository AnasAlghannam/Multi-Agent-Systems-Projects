# DocChat — Multi-Agent Document Q&A

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Ask questions about your own documents and get answers that are **checked before you see them**.

Upload PDFs, Word files, Markdown, or plain text, ask a question, and three agents work in
sequence: one decides whether your documents can actually answer the question, one drafts an answer
grounded in the retrieved passages, and one verifies that draft against the source material and
reports what it could and could not support. If verification fails, the workflow loops back and
re-researches rather than handing you an unchecked answer.

Everything runs locally except the language model calls — documents never leave your machine, and
embeddings are computed on your CPU.

## How it works

```
  question + documents
          │
          ▼
  ┌───────────────────┐   no relevant content
  │ RelevanceChecker  │ ─────────────────────▶ END ("ask something else")
  └───────────────────┘
          │ relevant / partial
          ▼
  ┌───────────────────┐
  │   ResearchAgent   │  drafts an answer from retrieved passages
  └───────────────────┘
          │
          ▼
  ┌───────────────────┐   unsupported or irrelevant
  │ VerificationAgent │ ──────────────────────┐
  └───────────────────┘                       │
          │ verified                          │
          ▼                                   ▼
         END                          back to ResearchAgent
```

**Retrieval is hybrid.** A BM25 keyword retriever and a Chroma vector store are blended with
`EnsembleRetriever` (weights in `config/settings.py`), so exact terms and paraphrased questions both
work. Documents are parsed with [Docling](https://github.com/DS4SD/docling), split on Markdown
headers, and cached by content hash so re-asking about the same file is fast.

## Project layout

| Path | Purpose |
|------|---------|
| `app.py` | Gradio UI and request handling |
| `agents/workflow.py` | LangGraph state machine wiring the three agents |
| `agents/relevance_checker.py` | Classifies coverage: `CAN_ANSWER` / `PARTIAL` / `NO_MATCH` |
| `agents/research_agent.py` | Drafts the answer from retrieved context |
| `agents/verification_agent.py` | Checks the draft against sources, emits a report |
| `retriever/builder.py` | Builds the hybrid BM25 + vector retriever |
| `document_processor/file_handler.py` | Docling parsing, chunking, content-hash caching |
| `utils/llm.py` | Single place where the chat model is configured |
| `config/` | Settings and constants |
| `verify_setup.py` | End-to-end check that the install and keys work |
| `test/test1.py` | Scratch script comparing Docling vs. PyPDF parsing on the sample fixtures |

## Setup

Run the project in its own virtual environment so its dependencies stay isolated.

```bash
cd DocChat
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Installation pulls in Docling and sentence-transformers and takes a few minutes. For the exact
versions this was built against, use `pip install -r requirements-lock.txt` instead.

### API key

```bash
cp .env.example .env
```

Edit `.env` and set `GROQ_API_KEY` — get one free at
[console.groq.com/keys](https://console.groq.com/keys). `.env` is git-ignored; never commit it.

Only the chat model needs a key. Embeddings run locally through sentence-transformers, so the
embedding model downloads once (about 90 MB) on first run and is cached afterwards.

## Verify the setup

Run these in order. Each one checks a specific layer, so a failure tells you exactly what is wrong.

**1. Imports and configuration**

```bash
python -c "from agents.workflow import AgentWorkflow; from retriever.builder import RetrieverBuilder; print('imports OK')"
```

**2. API key is loaded and the model answers**

```bash
python -c "from utils.llm import get_llm, complete; print(complete(get_llm(), 'Reply with exactly: OK'))"
```

Expect `OK`. A `RuntimeError` here means `.env` is missing or `GROQ_API_KEY` is unset.

**3. Full pipeline on the bundled sample** (downloads the embedding model on first run)

```bash
python verify_setup.py
```

This parses `examples/sample-solar-report.md`, builds the hybrid retriever, runs all three agents,
and prints the answer plus the verification report. It exits non-zero if any stage fails.

**4. Launch the app**

```bash
python app.py
```

Open <http://127.0.0.1:5000>. Upload a document, type a question, press **Submit**.

## Usage notes

- **Supported formats:** `.pdf`, `.docx`, `.txt`, `.md`
- **Size limits:** 50 MB per file, 200 MB total (`config/constants.py`)
- **First question about a document is slow** — it is parsed and embedded, then cached in
  `document_cache/` for a week (`CACHE_EXPIRE_DAYS`). Later questions reuse the cache.
- **The verification report is the point.** Read it alongside the answer — it lists unsupported
  claims and contradictions rather than hiding them.

### Configuration

Set these in `.env`:

| Variable | Default | Meaning |
|----------|---------|---------|
| `GROQ_API_KEY` | — | Required. |
| `DOCCHAT_MODEL` | `llama-3.3-70b-versatile` | Chat model for all three agents. |
| `DOCCHAT_PORT` | `5000` | Port for the UI. |
| `DOCCHAT_SHARE` | unset | Set to `1` to expose a public Gradio tunnel. Off by default so uploaded documents stay local. |

Retrieval behaviour (chunk counts, blend weights, cache lifetime, embedding model) lives in
`config/settings.py`.

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| `RuntimeError: GROQ_API_KEY is not set` | No `.env`, or the key line is blank. Copy `.env.example` and fill it in. |
| First run hangs at "Processing documents" | The embedding model is downloading (~90 MB). It only happens once. |
| `Port 5000 is in use` | On macOS, AirPlay Receiver takes port 5000. Set `DOCCHAT_PORT=7860` in `.env`, or turn it off in System Settings → General → AirDrop & Handoff. |
| Answers say the question is unrelated | The relevance checker found no matching passages. Try wording closer to the document, or confirm the file parsed (check `app.log`). |
| Rate-limit errors from the model provider | Free-tier quota. Wait, or set `DOCCHAT_MODEL` to a smaller model such as `llama-3.1-8b-instant`. |

## Adding your own examples

Drop files into `examples/` and add an entry to `EXAMPLES` in `app.py`:

```python
EXAMPLES = {
    "My Report": {
        "question": "What were the Q3 findings?",
        "file_paths": ["examples/my-report.pdf"],
    },
}
```
