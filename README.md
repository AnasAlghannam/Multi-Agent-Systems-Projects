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

### 2. [WorkflowPatternsLangGraph](WorkflowPatternsLangGraph/) — Coordination Patterns

The three ways to wire LLM calls together, each built end to end: **chaining** (sequential steps),
**routing** (a classifier picks the branch), and **parallelization** (independent steps run at once,
then merge). Closes with a multi-agent router dispatching to four specialized handlers.

**Stack:** LangGraph · Gradio · Groq

---

### 3. [OrchestrationEvaluationLangGraph](OrchestrationEvaluationLangGraph/) — Orchestration & Reflection

Two heavier patterns. **Orchestrator–Worker** plans a variable number of subtasks and fans them out
to parallel workers with `Send`, then merges the results. **Reflection** puts a generator and an
evaluator in a loop, revising until the output meets its target or an iteration cap trips.

**Stack:** LangGraph · Gradio · Groq

---

### 4. [NourishBot](NourishBot/) — Multi-Agent Nutrition Assistant

Four agents turn a set of ingredients into recipe ideas or a full nutritional analysis: one detects
ingredients (from an image where a vision model is available, otherwise a typed list), one applies
dietary restrictions, one estimates calories and nutrients, and one suggests recipes or evaluates
healthiness. Output is Pydantic-typed and rendered as tables in a Gradio UI.

**Stack:** CrewAI (`@CrewBase` + YAML config) · Gradio · Groq

[Watch the 23-second walkthrough →](NourishBot/brag-output/brag.mp4)

---

### 5. [BeeAIRequirementAgents](BeeAIRequirementAgents/) — Declaratively Constrained Agents

Eleven examples on the [BeeAI framework](https://github.com/i-am-bee/beeai-framework), from a single
chat call up to a four-agent travel planner. Its `RequirementAgent` constrains tool use
**declaratively** — think first, never search twice in a row, ask before handing off — so the rules
are enforced rather than merely prompted for. The capstone coordinates a destination expert, a
meteorologist and a language expert through `HandoffTool`.

**Stack:** BeeAI framework · Groq

---

### 6. [AG2AutoGenBasics](AG2AutoGenBasics/) — AG2 (AutoGen) Tutorial

A tour of AG2, the community fork of Microsoft's AutoGen: conversable agents, specialized roles,
human-in-the-loop review, `GroupChat` orchestration, tool registration, and typed outputs.

**Stack:** AG2 (AutoGen) · Groq

---

### 7. [AG2HealthcareChatbot](AG2HealthcareChatbot/) — Multi-Agent Consultation

A consultation assistant built as a group of narrow agents rather than one model — patient,
diagnosis and further specialists, coordinated by a `GroupChatManager` that picks the next speaker.
A second crew applies the same structure to emotional wellbeing. Demonstration only, not medical
advice.

**Stack:** AG2 (AutoGen) · Groq

---


### 8. [SpecializedAgentDesign](SpecializedAgentDesign/) — One Job Per Agent

Building agents that each own a narrow remit rather than one agent that tries to do everything:
role design, giving an agent only the tools its job needs, and boundaries on what it should attempt.

**Stack:** LangChain · Groq

---

### 9. [MultiAgentSystemImplementation](MultiAgentSystemImplementation/) — Composing Them

Wiring specialized agents into a working system: routing work between them, sharing state, and
deciding when the group is finished.

**Stack:** LangChain · Groq

---

### 10. [AgentChatbotInterface](AgentChatbotInterface/) — A Conversational Front End

Putting chat in front of a multi-agent system: intent classification routes each message to the
right agent, preferences are extracted from free text, and conversation state persists across turns.

**Stack:** LangChain · Gradio · Groq

---

> **MCP projects** live in a separate repo:
> [Model-Context-Protocol-Projects](https://github.com/AnasAlghannam/Model-Context-Protocol-Projects).

### Switching model provider

Every project reads its key from `.env`. Two providers are supported, and both speak the OpenAI
protocol, so switching is a matter of which key is present:

| Set this | Effect |
|---|---|
| `GROQ_API_KEY` | Default. Fast and free, but the free tier has a tight rate limit. |
| `OPENROUTER_API_KEY` | Takes priority when set. Fronts many models behind one key — useful when Groq's quota runs out, or when you need a model Groq does not host (vision models, for instance). |

Set `OPENROUTER_MODEL` to pick the model, e.g. `meta-llama/llama-3.3-70b-instruct`. Projects with a
central config module switch automatically; the rest name their model inline and take a one-line
edit.

### Tracing

Multi-agent runs are hard to debug from stdout — which agent ran, what it was sent, why it looped.
Setting Langfuse credentials in `.env` traces every model call and graph step to a dashboard:

```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Free tier at [cloud.langfuse.com](https://cloud.langfuse.com). Leave the keys blank and the projects
run exactly as before — tracing is additive, never required.

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
