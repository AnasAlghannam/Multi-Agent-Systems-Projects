# Implementing Multi-Agent Systems

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Wiring specialized agents into a working system: how work is routed between them, how state is shared, and how the group decides it is finished.

## What it covers
- Routing work between agents
- Shared state across a multi-agent run
- Termination conditions so a system does not loop forever
- Composing agents built and tested separately
- Tracing which agent handled which step

## Setup

```bash
cd MultiAgentSystemImplementation
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install langchain langchain-groq python-dotenv jupyter ipykernel
```

### API key

```bash
cp .env.example .env
```

Set `GROQ_API_KEY` — free at [console.groq.com/keys](https://console.groq.com/keys). `.env` is git-ignored.

## Run it

```bash
python -m ipykernel install --user --name MultiAgentSystemImplementation --display-name "Python (MultiAgentSystemImplementation)"
jupyter notebook "MultiAgentSystemImplementation.ipynb"
```

Select **Kernel → Change kernel → Python (MultiAgentSystemImplementation)**.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `GROQ_API_KEY` | — | Required. |
| `MODEL_ID` | `llama-3.3-70b-versatile` | Text model. |
| `BASE_URL` | `https://api.groq.com/openai/v1` | Any OpenAI-compatible endpoint. |
