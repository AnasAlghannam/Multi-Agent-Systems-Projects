"""Gradio front-end for trying each workflow pattern locally.

    python app.py     # then open http://127.0.0.1:7860
"""

import os

import gradio as gr

from workflows import (
    build_chain_workflow,
    build_routing_workflow,
    build_parallel_workflow,
    build_multi_agent_workflow,
)

# Graphs are compiled lazily so the UI still loads (and can show a readable
# error) when GROQ_API_KEY is missing.
_graphs = {}


def _graph(name, builder):
    if name not in _graphs:
        _graphs[name] = builder()
    return _graphs[name]


def run_chain(job_description):
    if not job_description.strip():
        return "Enter a job description first.", ""
    try:
        result = _graph("chain", build_chain_workflow).invoke(
            {"job_description": job_description, "resume_summary": "", "cover_letter": ""}
        )
    except Exception as e:
        return f"Error: {e}", ""
    return result["resume_summary"], result["cover_letter"]


def run_routing(user_input):
    if not user_input.strip():
        return "", "Enter some text first."
    try:
        result = _graph("routing", build_routing_workflow).invoke(
            {"user_input": user_input, "task_type": "", "output": ""}
        )
    except Exception as e:
        return "", f"Error: {e}"
    return result["task_type"], result["output"]


def run_parallel(text):
    if not text.strip():
        return "", "", "", "Enter some text first."
    try:
        result = _graph("parallel", build_parallel_workflow).invoke(
            {"text": text, "french": "", "spanish": "", "japanese": "", "combined_output": ""}
        )
    except Exception as e:
        return "", "", "", f"Error: {e}"
    return result["french"], result["spanish"], result["japanese"], result["combined_output"]


def run_multi_agent(user_input):
    if not user_input.strip():
        return "", "Enter a request first."
    try:
        result = _graph("multi", build_multi_agent_workflow).invoke(
            {"user_input": user_input, "task_type": "", "output": ""}
        )
    except Exception as e:
        return "", f"Error: {e}"
    return result["task_type"], result["output"]


def build_ui():
    with gr.Blocks(title="LangGraph Workflow Patterns") as demo:
        gr.Markdown("# LangGraph Workflow Patterns")
        gr.Markdown(
            "Try each pattern against a live model. Set `GROQ_API_KEY` in `.env` first."
        )

        with gr.Tab("1. Prompt Chaining"):
            gr.Markdown("Sequential steps: job description → resume summary → cover letter.")
            jd = gr.Textbox(label="Job description", lines=6)
            chain_btn = gr.Button("Run chain", variant="primary")
            summary_out = gr.Textbox(label="Resume summary", lines=6)
            letter_out = gr.Textbox(label="Cover letter", lines=10)
            chain_btn.click(run_chain, inputs=jd, outputs=[summary_out, letter_out])
            gr.Examples(
                [["We are hiring a data scientist with 3+ years of Python, SQL and "
                  "machine learning experience to build forecasting models."]],
                inputs=jd,
            )

        with gr.Tab("2. Routing"):
            gr.Markdown("A classifier picks the branch: summarize or translate.")
            route_in = gr.Textbox(label="Your request", lines=4)
            route_btn = gr.Button("Run router", variant="primary")
            route_type = gr.Textbox(label="Chosen branch")
            route_out = gr.Textbox(label="Result", lines=8)
            route_btn.click(run_routing, inputs=route_in, outputs=[route_type, route_out])
            gr.Examples(
                [["Summarize this: the solar array produced 12% more energy this quarter "
                  "after the panels were cleaned and realigned."],
                 ["Translate to French: the weather is beautiful today."]],
                inputs=route_in,
            )

        with gr.Tab("3. Parallelization"):
            gr.Markdown("Three translations run at the same time, then get merged.")
            par_in = gr.Textbox(label="English text", lines=3)
            par_btn = gr.Button("Translate in parallel", variant="primary")
            with gr.Row():
                fr = gr.Textbox(label="French", lines=3)
                es = gr.Textbox(label="Spanish", lines=3)
                ja = gr.Textbox(label="Japanese", lines=3)
            merged = gr.Textbox(label="Merged output", lines=8)
            par_btn.click(run_parallel, inputs=par_in, outputs=[fr, es, ja, merged])
            gr.Examples([["The train arrives at nine in the morning."]], inputs=par_in)

        with gr.Tab("4. Multi-Agent Router"):
            gr.Markdown(
                "Routes to one of four handlers: ride hailing, restaurant order, "
                "groceries, or a fallback."
            )
            ma_in = gr.Textbox(label="Your request", lines=3)
            ma_btn = gr.Button("Route request", variant="primary")
            ma_type = gr.Textbox(label="Handler chosen")
            ma_out = gr.Textbox(label="Response", lines=10)
            ma_btn.click(run_multi_agent, inputs=ma_in, outputs=[ma_type, ma_out])
            gr.Examples(
                [["I need a ride from downtown to the airport at 3pm"],
                 ["I want to order 2 large pepperoni pizzas for delivery"],
                 ["I need milk, bread, eggs and vegetables for the week"],
                 ["What's the weather like today?"]],
                inputs=ma_in,
            )

    return demo


if __name__ == "__main__":
    build_ui().launch(
        server_name="127.0.0.1",
        server_port=int(os.environ.get("APP_PORT", 7860)),
        # share=True would expose this through a public tunnel; opt in explicitly.
        share=os.environ.get("APP_SHARE") == "1",
    )
