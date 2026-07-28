"""The four LangGraph workflows, built once and shared by the notebook and the Gradio app.

Each `build_*` function returns a compiled graph you can `.invoke()`.
"""

from typing import TypedDict

from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

load_dotenv(find_dotenv(usecwd=True))

import os

from langchain_groq import ChatGroq

MODEL = os.environ.get("WORKFLOW_MODEL", "llama-3.3-70b-versatile")


def get_llm(temperature: float = 0.0) -> ChatGroq:
    """Return the chat model, failing with a clear message if the key is missing."""
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com/keys)."
        )
    return ChatGroq(model=MODEL, temperature=temperature)


# --------------------------------------------------------------------------
# 1. Prompt chaining - job application assistant
# --------------------------------------------------------------------------

class ChainState(TypedDict):
    job_description: str
    resume_summary: str
    cover_letter: str


def build_chain_workflow():
    """Sequential: job description -> resume summary -> cover letter."""
    llm = get_llm()

    def generate_resume_summary(state: ChainState) -> ChainState:
        prompt = (
            "You're a resume assistant. Read the following job description and summarize "
            "the key qualifications and experience the ideal candidate should have, phrased "
            "as a strong applicant's resume summary.\n\n"
            f"Job Description:\n{state['job_description']}"
        )
        return {**state, "resume_summary": llm.invoke(prompt).content}

    def generate_cover_letter(state: ChainState) -> ChainState:
        prompt = (
            "You're a cover letter assistant. Using the resume summary below, write a "
            "professional, personalized cover letter for the job.\n\n"
            f"Resume Summary:\n{state['resume_summary']}\n\n"
            f"Job Description:\n{state['job_description']}"
        )
        return {**state, "cover_letter": llm.invoke(prompt).content}

    workflow = StateGraph(ChainState)
    workflow.add_node("generate_resume_summary", generate_resume_summary)
    workflow.add_node("generate_cover_letter", generate_cover_letter)
    workflow.set_entry_point("generate_resume_summary")
    workflow.add_edge("generate_resume_summary", "generate_cover_letter")
    workflow.set_finish_point("generate_cover_letter")
    return workflow.compile()


# --------------------------------------------------------------------------
# 2. Routing - summarize or translate
# --------------------------------------------------------------------------

class RouterState(TypedDict):
    user_input: str
    task_type: str
    output: str


class TaskRoute(BaseModel):
    role: str = Field(
        ...,
        description="Classify the request. Return exactly one of: 'summarize', 'translate'.",
    )


def build_routing_workflow():
    """Classify the request, then run the matching branch."""
    llm = get_llm()
    llm_router = llm.bind_tools([TaskRoute])

    def router_node(state: RouterState) -> RouterState:
        prompt = (
            "Classify whether the user wants to 'summarize' a passage or 'translate' text.\n\n"
            f"User Input: {state['user_input']}"
        )
        try:
            response = llm_router.invoke(prompt)
        except Exception:
            # Some hosted models emit a malformed tool call and the API rejects it.
            # Classification failing should not take the whole graph down.
            return {**state, "task_type": "summarize"}

        if response.tool_calls:
            label = response.tool_calls[0]["args"].get("role", "")
            if label in ("summarize", "translate"):
                return {**state, "task_type": label}
        return {**state, "task_type": "summarize"}

    def router(state: RouterState) -> str:
        return state["task_type"]

    def summarize_node(state: RouterState) -> RouterState:
        response = llm.invoke(f"Summarize the following passage:\n\n{state['user_input']}")
        return {**state, "task_type": "summarize", "output": response.content}

    def translate_node(state: RouterState) -> RouterState:
        response = llm.invoke(f"Translate the following text to French:\n\n{state['user_input']}")
        return {**state, "task_type": "translate", "output": response.content}

    workflow = StateGraph(RouterState)
    workflow.add_node("router", router_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("translate", translate_node)
    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router", router, {"summarize": "summarize", "translate": "translate"}
    )
    workflow.set_finish_point("summarize")
    workflow.set_finish_point("translate")
    return workflow.compile()


# --------------------------------------------------------------------------
# 3. Parallelization - multilingual translation
# --------------------------------------------------------------------------

class ParallelState(TypedDict):
    text: str
    french: str
    spanish: str
    japanese: str
    combined_output: str


def build_parallel_workflow():
    """Three translations run concurrently, then an aggregator merges them."""
    llm = get_llm()

    def translate_french(state: ParallelState) -> dict:
        return {"french": llm.invoke(f"Translate to French:\n\n{state['text']}").content.strip()}

    def translate_spanish(state: ParallelState) -> dict:
        return {"spanish": llm.invoke(f"Translate to Spanish:\n\n{state['text']}").content.strip()}

    def translate_japanese(state: ParallelState) -> dict:
        return {"japanese": llm.invoke(f"Translate to Japanese:\n\n{state['text']}").content.strip()}

    def aggregator(state: ParallelState) -> dict:
        combined = (
            f"Original: {state['text']}\n\n"
            f"French: {state['french']}\n\n"
            f"Spanish: {state['spanish']}\n\n"
            f"Japanese: {state['japanese']}\n"
        )
        return {"combined_output": combined}

    graph = StateGraph(ParallelState)
    graph.add_node("translate_french", translate_french)
    graph.add_node("translate_spanish", translate_spanish)
    graph.add_node("translate_japanese", translate_japanese)
    graph.add_node("aggregator", aggregator)

    # Fan out from START so the three translations run in parallel...
    graph.add_edge(START, "translate_french")
    graph.add_edge(START, "translate_spanish")
    graph.add_edge(START, "translate_japanese")
    # ...then fan in to the aggregator.
    graph.add_edge("translate_french", "aggregator")
    graph.add_edge("translate_spanish", "aggregator")
    graph.add_edge("translate_japanese", "aggregator")
    graph.add_edge("aggregator", END)
    return graph.compile()


# --------------------------------------------------------------------------
# 4. Multi-agent routing - four specialized handlers
# --------------------------------------------------------------------------

class ServiceRoute(BaseModel):
    role: str = Field(
        ...,
        description=(
            "Classify the user request. Return exactly one of: 'ride_hailing_call', "
            "'restaurant_order', 'groceries'. If unsure, return 'default_handler'."
        ),
    )


def build_multi_agent_workflow():
    """Dispatch a request to one of four specialized handlers."""
    llm = get_llm()
    llm_router = llm.bind_tools([ServiceRoute])

    VALID = {"ride_hailing_call", "restaurant_order", "groceries", "default_handler"}

    def router_node(state: RouterState) -> RouterState:
        try:
            response = llm_router.invoke(state["user_input"])
        except Exception:
            # A request the model cannot classify sometimes comes back as a
            # malformed tool call, which the API rejects. That is precisely the
            # case default_handler exists for, so route there instead of raising.
            return {**state, "task_type": "default_handler"}

        if response.tool_calls:
            label = response.tool_calls[0]["args"].get("role", "")
            if label in VALID:
                return {**state, "task_type": label}
        return {**state, "task_type": "default_handler"}

    def router(state: RouterState) -> str:
        return state["task_type"]

    def _handler(system_prompt: str):
        """Build a handler node that answers with the given persona."""
        def node(state: RouterState) -> RouterState:
            response = llm.invoke(f"{system_prompt}\n\nRequest: {state['user_input']}")
            return {**state, "output": response.content}
        return node

    workflow = StateGraph(RouterState)
    workflow.add_node("router", router_node)
    workflow.add_node(
        "ride_hailing_call",
        _handler("You are a ride hailing agent. Confirm pickup, destination and time, "
                 "then give an estimated fare and arrival."),
    )
    workflow.add_node(
        "restaurant_order",
        _handler("You are a restaurant order agent. Confirm the items, quantities and "
                 "delivery details, then give an estimated total and delivery time."),
    )
    workflow.add_node(
        "groceries",
        _handler("You are a grocery agent. Turn the request into an itemized shopping "
                 "list with quantities and an estimated total."),
    )
    workflow.add_node(
        "default_handler",
        _handler("You are a general assistant. The request did not match a supported "
                 "service, so answer helpfully and mention what services are available: "
                 "ride hailing, restaurant orders, and groceries."),
    )

    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        router,
        {
            "ride_hailing_call": "ride_hailing_call",
            "restaurant_order": "restaurant_order",
            "groceries": "groceries",
            "default_handler": "default_handler",
        },
    )
    for node in ("ride_hailing_call", "restaurant_order", "groceries", "default_handler"):
        workflow.set_finish_point(node)
    return workflow.compile()
