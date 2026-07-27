# Multi-Agent Systems Projects

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Applications built around **multiple AI agents working together** — each agent owning a role, with
an orchestration layer routing work between them and deciding when the job is done.

Each project lives in its own folder with a self-contained README covering setup, configuration, and
how to verify it works.

---

## Projects

### 1. [DocChat](DocChat/) — Multi-Agent Document Q&A

Ask questions about your own documents and get answers that are **checked before you see them**.
Three agents run in sequence: one decides whether the documents can answer the question at all, one
drafts an answer from the retrieved passages, and one verifies that draft against the sources and
reports what it could not support. Failed verification loops back for another pass.

**Stack:** LangGraph · Gradio · Docling · Chroma + BM25 hybrid retrieval · Groq

**Agents:** `RelevanceChecker` → `ResearchAgent` → `VerificationAgent`

---

## Conventions

Every project in this repo follows the same rules:

- **Isolated environment.** Each project has its own virtualenv; dependencies never collide.
- **No secrets in git.** Keys are read from a `.env` file that is git-ignored. Each project ships a
  `.env.example` listing what it needs and where to get it.
- **Verifiable setup.** Each project includes a way to confirm the install actually works before you
  start using it, rather than leaving you to debug a wall of tracebacks.

## Getting started

```bash
cd <ProjectFolder>
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env                 # then fill in your API keys
```

See the project's own README for the verification steps and how to run it.
