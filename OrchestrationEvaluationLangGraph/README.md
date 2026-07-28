# LangGraph Orchestration & Evaluation

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

Two agentic design patterns, each built end to end and runnable from a local web UI.

| Pattern | What it does | Example built here |
|---------|--------------|--------------------|
| **Orchestrator–Worker** | A planner splits a request into a variable number of subtasks, workers handle them in parallel, a synthesizer merges the results | Meal planner: meals → per-dish cooking guides → one combined guide |
| **Reflection (evaluator–optimizer)** | A generator proposes, an evaluator grades, and the loop repeats until the output hits its target | Investment advisor that revises until the plan's risk matches the profile |

## Shapes

```
Orchestrator-Worker:
                        ┌──▶ chef_worker ──┐
    START ──▶ orchestrator ──▶ chef_worker ──┼──▶ synthesizer ──▶ END
                        └──▶ chef_worker ──┘
              (one worker per dish, fanned out with Send)

Reflection:
    START ──▶ determine_target_grade ──▶ generator ──▶ evaluator
                                            ▲              │
                                            └── feedback ───┤ grade != target
                                                            │
                                                           END  grade == target
                                                                (or iteration cap)
```

Two details make these work:

- **`Send`** fans out one worker per subtask at runtime, so the graph doesn't need to know the
  subtask count in advance.
- **`Annotated[List[str], operator.add]`** lets parallel workers each append to the same state key
  instead of overwriting one another.

## Layout

| Path | Purpose |
|------|---------|
| `OrchestrationEvaluationLangGraph.ipynb` | Walkthrough building both patterns step by step |
| `workflows.py` | The two compiled graphs, shared by the notebook and the app |
| `app.py` | Gradio UI with a tab per pattern |
| `verify_setup.py` | End-to-end check that the install and key work |

## Setup

```bash
cd OrchestrationEvaluationLangGraph
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

**1. Key and model**

```bash
python -c "from workflows import get_llm; print(get_llm().invoke('Reply with exactly: OK').content)"
```

**2. Both workflows end to end**

```bash
python verify_setup.py
```

Plans a two-dish menu in parallel and runs the reflection loop to convergence. Exits non-zero on
failure.

**3. Launch the UI**

```bash
python app.py
```

Open <http://127.0.0.1:7861>. Each tab has example inputs.

## Running the notebook

```bash
python -m ipykernel install --user --name OrchestrationEvaluationLangGraph --display-name "Python (OrchestrationEvaluationLangGraph)"
jupyter notebook "OrchestrationEvaluationLangGraph.ipynb"
```

Select the matching kernel via **Kernel → Change kernel**.

## Configuration

| Variable | Default | Meaning |
|----------|---------|---------|
| `GROQ_API_KEY` | — | Required. |
| `WORKFLOW_MODEL` | `llama-3.3-70b-versatile` | Model used by both workflows. |
| `APP_PORT` | `7861` | Port for the Gradio UI. |
| `APP_SHARE` | unset | Set to `1` to expose a public tunnel. Off by default. |

The reflection loop's iteration cap is a parameter: `build_investment_workflow(iteration_limit=5)`.
Without a cap, a generator and evaluator that never agree would loop forever.

## Disclaimer

The investment example demonstrates the reflection pattern. It is not financial advice, and the
plans it produces are LLM output with no grounding in real market data.
