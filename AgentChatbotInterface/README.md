# Building a Chatbot Interface for Agents

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Putting a conversational front end on a multi-agent system, so the agents are reachable through ordinary chat while conversation state persists across turns.

## What it covers
- Intent classification to route a message to the right agent
- Extracting structured preferences from free-form text
- Carrying conversation history across turns
- Presenting agent output as readable chat replies
- Graceful failure when a downstream call errors

## Setup

```bash
cd AgentChatbotInterface
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install langchain langchain-groq gradio python-dotenv jupyter ipykernel
```

### API key

```bash
cp .env.example .env
```

Set `GROQ_API_KEY` — free at [console.groq.com/keys](https://console.groq.com/keys). `.env` is git-ignored.

## Run it

```bash
python -m ipykernel install --user --name AgentChatbotInterface --display-name "Python (AgentChatbotInterface)"
jupyter notebook "AgentChatbotInterface.ipynb"
```

Select **Kernel → Change kernel → Python (AgentChatbotInterface)**.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `GROQ_API_KEY` | — | Required. |
| `MODEL_ID` | `llama-3.3-70b-versatile` | Text model. |
| `BASE_URL` | `https://api.groq.com/openai/v1` | Any OpenAI-compatible endpoint. |
