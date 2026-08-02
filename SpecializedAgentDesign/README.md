# Designing Specialized Agents

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Building agents that each own one narrow job rather than one agent that tries to do everything. Covers giving an agent a role, the tools it needs, and boundaries on what it should attempt — the groundwork for composing several of them into a system.

## What it covers
- Role and system-message design for a narrow remit
- Giving an agent only the tools its job requires
- Structured output so results are parseable
- Testing an agent in isolation before composing it
- Boundaries that stop an agent overreaching

## Setup

```bash
cd SpecializedAgentDesign
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
python -m ipykernel install --user --name SpecializedAgentDesign --display-name "Python (SpecializedAgentDesign)"
jupyter notebook "SpecializedAgentDesign.ipynb"
```

Select **Kernel → Change kernel → Python (SpecializedAgentDesign)**.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `GROQ_API_KEY` | — | Required. |
| `MODEL_ID` | `llama-3.3-70b-versatile` | Text model. |
| `BASE_URL` | `https://api.groq.com/openai/v1` | Any OpenAI-compatible endpoint. |
