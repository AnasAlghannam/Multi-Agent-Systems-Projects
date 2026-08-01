# BeeAI Requirement Agents

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Agents built with the [BeeAI framework](https://github.com/i-am-bee/beeai-framework), worked up from
a single chat call to a four-agent travel planner that delegates between specialists.

What makes BeeAI's `RequirementAgent` distinctive is that tool use is **constrained declaratively**.
Instead of hoping the model calls the right tool, you state the rules — think first, never call
search twice in a row, ask before handing off — and the framework enforces them.

## The examples

| # | File | What it shows |
|---|------|---------------|
| 01 | `01_basic_chat.py` | A single chat call with system and user messages |
| 02 | `02_prompt_templates.py` | Reusable prompt templates |
| 03 | `03_structured_output.py` | Pydantic-typed responses via `response_format` |
| 04 | `04_minimal_agent.py` | The smallest useful `RequirementAgent` |
| 05 | `05_agent_with_wikipedia.py` | Giving an agent a search tool |
| 06 | `06_agent_with_reasoning.py` | `ThinkTool` for explicit reasoning steps |
| 07 | `07_controlled_execution.py` | `ConditionalRequirement`: force, order and cap tool calls |
| 08 | `08_reasoning_requirements.py` | Combining reasoning with tool constraints |
| 09 | `09_permissions_and_safety.py` | `AskPermissionRequirement` before sensitive actions |
| 10 | `10_custom_tool_calculator.py` | Writing a custom tool |
| 11 | `11_multi_agent_travel_planner.py` | Four agents coordinating through `HandoffTool` |

### The capstone

`11_multi_agent_travel_planner.py` runs four specialists:

```
                    ┌──────────────────────┐
   traveller ──▶    │  Travel Coordinator  │
                    └──────────────────────┘
                       │        │        │      HandoffTool
          ┌────────────┘        │        └────────────┐
          ▼                     ▼                     ▼
  Destination Expert     Meteorologist       Language & Culture
  (Wikipedia, Think)     (OpenMeteo, Think)  (Wikipedia, Think)
```

The coordinator delegates through `HandoffTool`, each specialist is bound by its own
`ConditionalRequirement`s (think first, then search, capped invocations), and
`AskPermissionRequirement` makes the coordinator ask before consulting anyone.

## Setup

```bash
cd BeeAIRequirementAgents
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

BeeAI addresses models as `provider:model` and ships providers for groq, openai, watsonx, ollama,
anthropic, gemini and others. Everything here routes through `config.py`, so switching provider is
one edit — or two environment variables:

```
BEEAI_PROVIDER=ollama
BEEAI_MODEL=llama3.1
```

## Verify it works

```bash
python verify_setup.py           # key, model and imports
python verify_setup.py --all     # run every example (slow, makes many calls)
```

Then run any example directly:

```bash
python examples/01_basic_chat.py
python examples/11_multi_agent_travel_planner.py
```

## Notes

- **Two examples wait for input.** `09` and `11` use `AskPermissionRequirement`, which prompts on
  the terminal before a tool runs. `verify_setup.py --all` skips them; run those two by hand.
- **`RequirementAgent` lives in `beeai_framework.agents.requirement`.** Older BeeAI code imports it
  from `agents.experimental`, which is deprecated and warns on import — these examples use the
  current path.
- **The tools reach the network.** `WikipediaTool` and `OpenMeteoTool` call public APIs, so those
  examples need connectivity but no extra keys.
- **Watch the rate limit.** The agent examples make many calls per run — reasoning, tool use, then a
  final answer — so running them back to back can exhaust a free-tier quota and surface as
  `ChatModelError` wrapping a 429. Wait a minute, or switch to a lighter model:

  ```bash
  BEEAI_MODEL=llama-3.1-8b-instant python examples/06_agent_with_reasoning.py
  ```
