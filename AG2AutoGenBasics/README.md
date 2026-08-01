# AG2 (AutoGen) — Multi-Agent Systems Tutorial

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

A tour of [AG2](https://github.com/ag2ai/ag2) — the community fork of Microsoft's AutoGen — built up
from a two-agent conversation to orchestrated group chats with tools and typed output.

## What it covers

| Concept | What it does |
|---------|--------------|
| `ConversableAgent` | The base unit: a system message plus the ability to converse |
| Specialized agents | Distinct roles from distinct system messages |
| `AssistantAgent` / `UserProxyAgent` | The built-in assistant/executor pair |
| Human-in-the-loop | `human_input_mode` decides when a person is consulted |
| `GroupChat` / `GroupChatManager` | Orchestration when more than two agents are involved |
| `register_function` | Tools, with calling and execution split across agents |
| Structured outputs | Pydantic `response_format` for typed replies instead of prose |

## Setup

```bash
cd AG2AutoGenBasics
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### API key

```bash
cp .env.example .env
```

Set `GROQ_API_KEY` — free at [console.groq.com/keys](https://console.groq.com/keys). `.env` is
git-ignored.

AG2 works with any OpenAI-compatible endpoint, so `config.py` simply points it at Groq via
`base_url`. To use a different provider, change `AG2_BASE_URL` and `AG2_MODEL` in `.env`.

## Run it

```bash
python -m ipykernel install --user --name AG2AutoGenBasics --display-name "Python (AG2AutoGenBasics)"
jupyter notebook "AG2AutoGenBasics.ipynb"
```

Select the matching kernel via **Kernel → Change kernel**.

## Configuration

| Variable | Default | Meaning |
|----------|---------|---------|
| `GROQ_API_KEY` | — | Required. |
| `AG2_MODEL` | `llama-3.3-70b-versatile` | Model used by every agent. |
| `AG2_BASE_URL` | `https://api.groq.com/openai/v1` | Any OpenAI-compatible endpoint. |

## Note on the AG2 version

`requirements.txt` pins **`ag2[openai]<1.0` deliberately**. AG2 1.0 renamed the module from
`autogen` to `ag2` and replaced `ConversableAgent`, `GroupChat` and `GroupChatManager` with a
different API — so on 1.x every import here fails. The 0.x line is what this material is written
against; upgrading means rewriting the agent code, not just the imports.
