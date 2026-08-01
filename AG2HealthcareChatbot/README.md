# Multi-Agent Healthcare Chatbot with AG2 (AutoGen)

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

A consultation assistant built as a **group of specialized agents** rather than one model. A patient
agent describes symptoms, a diagnosis agent interprets them, and further specialists weigh in — all
coordinated by a `GroupChatManager` that decides who speaks next.

A second crew at the end applies the same structure to emotional wellbeing, showing that the
orchestration pattern, not the domain, is what carries over.

## What it covers

| Concept | What it does |
|---------|--------------|
| `ConversableAgent` | One agent per role, each with its own system message |
| `GroupChat` | Holds the agents and the shared transcript, capped by `max_round` |
| `GroupChatManager` | Picks the next speaker from the conversation so far |
| Role separation | Narrow remits instead of one general-purpose prompt |

## Disclaimer

**Not medical advice.** This demonstrates a multi-agent architecture. Output is LLM-generated and
can be wrong — consult a qualified clinician for anything real.

## Setup

```bash
cd AG2HealthcareChatbot
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
python -m ipykernel install --user --name AG2HealthcareChatbot --display-name "Python (AG2HealthcareChatbot)"
jupyter notebook "AG2HealthcareChatbot.ipynb"
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
