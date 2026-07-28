# LangGraph Workflow Patterns

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Three patterns for turning individual LLM calls into a coordinated system, each built end to end and
runnable from a local web UI.

| Pattern | What it does | Example built here |
|---------|--------------|--------------------|
| **Prompt chaining** | Steps run in sequence, each consuming the previous output | Job description → resume summary → cover letter |
| **Routing** | A classifier sends each request down the matching branch | Summarize vs. translate |
| **Parallelization** | Independent steps run at once, then merge | One sentence → French, Spanish, Japanese |
| **Multi-agent routing** | Routing scaled to several specialized handlers | Ride hailing / restaurant / groceries / fallback |

## Shapes

```
Chaining:        A ──▶ B ──▶ C

Routing:              ┌──▶ summarize
            router ───┤
                      └──▶ translate

Parallelization:      ┌──▶ french   ──┐
            START ────┼──▶ spanish  ──┼──▶ aggregator ──▶ END
                      └──▶ japanese ──┘
```

## Layout

| Path | Purpose |
|------|---------|
| `WorkflowPatternsLangGraph.ipynb` | Walkthrough building each pattern step by step |
| `workflows.py` | The four compiled graphs, shared by the notebook and the app |
| `app.py` | Gradio UI with a tab per pattern |

## Setup

```bash
cd WorkflowPatternsLangGraph
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### API key

```bash
cp .env.example .env
```

Set `GROQ_API_KEY` in `.env` — free at [console.groq.com/keys](https://console.groq.com/keys).
`.env` is git-ignored.

## Verify it works

**1. Imports and key**

```bash
python -c "from workflows import get_llm; print(get_llm().invoke('Reply with exactly: OK').content)"
```

Expect `OK`. A `RuntimeError` means `.env` is missing or the key is unset.

**2. All four graphs compile and run**

```bash
python verify_setup.py
```

Runs each pattern against the live model and prints the result. Exits non-zero on failure.

**3. Launch the UI**

```bash
python app.py
```

Open <http://127.0.0.1:7860>. Each tab has example inputs — click one and press the button.

## Running the notebook

```bash
python -m ipykernel install --user --name WorkflowPatternsLangGraph --display-name "Python (WorkflowPatternsLangGraph)"
jupyter notebook "WorkflowPatternsLangGraph.ipynb"
```

Select the matching kernel via **Kernel → Change kernel**.

## Configuration

| Variable | Default | Meaning |
|----------|---------|---------|
| `GROQ_API_KEY` | — | Required. |
| `WORKFLOW_MODEL` | `llama-3.3-70b-versatile` | Model used by every workflow. |
| `APP_PORT` | `7860` | Port for the Gradio UI. |
| `APP_SHARE` | unset | Set to `1` to expose a public tunnel. Off by default. |

## Notes

- The routing patterns bind a Pydantic model as a **tool** so the classification comes back
  structured rather than parsed out of prose. Both routers fall back to a default branch when the
  model returns no tool call, so an unclassifiable request never crashes the graph.
- Parallel nodes each return only their own key. LangGraph merges those partial updates into the
  shared state, which is what makes concurrent fan-out safe.
