"""Gradio front-end for the orchestration and reflection workflows.

    python app.py     # then open http://127.0.0.1:7861
"""

import os

import gradio as gr

from workflows import build_meal_workflow, build_investment_workflow

_graphs = {}


def _graph(name, builder):
    if name not in _graphs:
        _graphs[name] = builder()
    return _graphs[name]


def run_meals(meals):
    if not meals.strip():
        return "Enter one or more meals first.", ""
    try:
        result = _graph("meals", build_meal_workflow).invoke(
            {"meals": meals, "sections": [], "completed_menu": [], "final_meal_guide": ""}
        )
    except Exception as e:
        return f"Error: {e}", ""
    dishes = "\n".join(
        f"- {d.name} ({d.location}): {', '.join(d.ingredients)}" for d in result["sections"]
    )
    return dishes, result["final_meal_guide"]


def run_investment(profile, limit):
    if not profile.strip():
        return "", "", "", "Enter an investor profile first."
    try:
        result = build_investment_workflow(iteration_limit=int(limit)).invoke(
            {
                "investor_profile": profile,
                "investment_plan": "",
                "target_grade": "",
                "feedback": "",
                "grade": "",
                "n": 0,
            }
        )
    except Exception as e:
        return "", "", "", f"Error: {e}"
    return (
        result.get("target_grade", ""),
        result.get("grade", ""),
        str(result.get("n", 0)),
        f"{result.get('investment_plan','')}\n\n---\nEvaluator feedback:\n{result.get('feedback','')}",
    )


def build_ui():
    with gr.Blocks(title="Orchestration & Evaluation") as demo:
        gr.Markdown("# LangGraph: Orchestration & Evaluation")
        gr.Markdown("Set `GROQ_API_KEY` in `.env` before running.")

        with gr.Tab("Orchestrator–Worker"):
            gr.Markdown(
                "A planner splits the meals into dishes, one worker per dish runs in "
                "parallel, and a synthesizer merges the results."
            )
            meals_in = gr.Textbox(label="Meals to prepare", lines=2)
            meals_btn = gr.Button("Plan meals", variant="primary")
            dishes_out = gr.Textbox(label="Dishes the planner produced", lines=5)
            guide_out = gr.Textbox(label="Combined cooking guide", lines=18)
            meals_btn.click(run_meals, inputs=meals_in, outputs=[dishes_out, guide_out])
            gr.Examples(
                [["banana smoothie, carrot cake"], ["chicken curry, greek salad, miso soup"]],
                inputs=meals_in,
            )

        with gr.Tab("Reflection Loop"):
            gr.Markdown(
                "A generator drafts a plan, an evaluator grades its risk level, and the loop "
                "repeats until the grade matches the target or the cap is reached.\n\n"
                "*Demonstration of the pattern — not financial advice.*"
            )
            profile_in = gr.Textbox(label="Investor profile", lines=4)
            limit_in = gr.Slider(1, 5, value=3, step=1, label="Max iterations")
            inv_btn = gr.Button("Generate plan", variant="primary")
            with gr.Row():
                target_out = gr.Textbox(label="Target grade")
                final_out = gr.Textbox(label="Final grade")
                iters_out = gr.Textbox(label="Iterations")
            plan_out = gr.Textbox(label="Plan and feedback", lines=18)
            inv_btn.click(
                run_investment,
                inputs=[profile_in, limit_in],
                outputs=[target_out, final_out, iters_out, plan_out],
            )
            gr.Examples(
                [["I am 28, saving for retirement in 35 years, comfortable with volatility."],
                 ["I am 63 and retiring in two years. Preserving capital matters most."]],
                inputs=profile_in,
            )

    return demo


if __name__ == "__main__":
    build_ui().launch(
        server_name="127.0.0.1",
        server_port=int(os.environ.get("APP_PORT", 7861)),
        # share=True would expose this publicly; opt in explicitly.
        share=os.environ.get("APP_SHARE") == "1",
    )
