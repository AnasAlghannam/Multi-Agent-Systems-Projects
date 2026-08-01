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

### 8. [MCPServerAgents](MCPServerAgents/) — Model Context Protocol

Using tools that live in a separate process. Covers the stdio and HTTP transports, listing a
server's tools and reading their schemas, then wiring two public MCP servers into one LangGraph
ReAct agent.

**Stack:** FastMCP · LangGraph · Groq

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
