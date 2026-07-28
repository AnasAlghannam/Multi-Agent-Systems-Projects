"""The two workflows, built once and shared by the notebook and the Gradio app.

Each `build_*` function returns a compiled graph you can `.invoke()`.

The investment workflow is a demonstration of the reflection pattern, not
financial advice.
"""

import operator
import os
from typing import Annotated, List, Literal, TypedDict

from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from pydantic import BaseModel, Field

load_dotenv(find_dotenv(usecwd=True))

from langchain_groq import ChatGroq

MODEL = os.environ.get("WORKFLOW_MODEL", "llama-3.3-70b-versatile")


def get_llm(temperature: float = 0.7) -> ChatGroq:
    """Return the chat model, failing with a clear message if the key is missing."""
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com/keys)."
        )
    return ChatGroq(model=MODEL, temperature=temperature)


# --------------------------------------------------------------------------
# Orchestrator-Worker: parallel meal planning
# --------------------------------------------------------------------------

class Dish(BaseModel):
    name: str = Field(description="Name of the dish.")
    ingredients: List[str] = Field(description="Ingredients needed for this dish.")
    location: str = Field(description="Cuisine or cultural origin of the dish.")


class Dishes(BaseModel):
    sections: List[Dish] = Field(description="One entry per dish to prepare.")


class MealState(TypedDict):
    meals: str
    sections: List[Dish]
    # operator.add lets parallel workers append rather than overwrite.
    completed_menu: Annotated[List[str], operator.add]
    final_meal_guide: str


class WorkerState(TypedDict):
    section: Dish
    completed_menu: Annotated[list, operator.add]


def build_meal_workflow():
    """Plan dishes, cook them in parallel, then merge into one guide."""
    llm = get_llm()

    planner_pipe = ChatPromptTemplate.from_messages([
        ("system",
         "You generate a structured dish list.\n\n"
         "The user wants to prepare: {meals}\n\n"
         "For each meal return the dish name, its ingredients, and its cuisine of origin."),
    ]) | llm.with_structured_output(Dishes)

    chef_pipe = ChatPromptTemplate.from_messages([
        ("system",
         "You are a chef from {location}. Present a detailed walkthrough for preparing "
         "{name}.\n\nInclude a short introduction, a list of preparation steps, and the "
         "cooking process. Use these ingredients: {ingredients}."),
    ]) | llm

    def orchestrator(state: MealState):
        """Split the meal request into structured dish sections."""
        return {"sections": planner_pipe.invoke({"meals": state["meals"]}).sections}

    def assign_workers(state: MealState):
        """Fan out one worker per dish - this is what makes them run in parallel."""
        return [Send("chef_worker", {"section": s}) for s in state["sections"]]

    def chef_worker(state: WorkerState):
        """Write the cooking section for a single dish."""
        section = state["section"]
        result = chef_pipe.invoke({
            "name": section.name,
            "location": section.location,
            "ingredients": ", ".join(section.ingredients),
        })
        return {"completed_menu": [result.content]}

    def synthesizer(state: MealState):
        """Concatenate the finished sections into one guide."""
        return {"final_meal_guide": "\n\n---\n\n".join(state["completed_menu"])}

    builder = StateGraph(MealState)
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("chef_worker", chef_worker)
    builder.add_node("synthesizer", synthesizer)
    builder.add_edge(START, "orchestrator")
    builder.add_conditional_edges("orchestrator", assign_workers, ["chef_worker"])
    builder.add_edge("chef_worker", "synthesizer")
    builder.add_edge("synthesizer", END)
    return builder.compile()


# --------------------------------------------------------------------------
# Reflection: iterative investment-plan refinement
# --------------------------------------------------------------------------

grades = Literal["ultra-conservative", "conservative", "moderate", "aggressive", "high risk"]


class InvestState(TypedDict):
    investment_plan: str
    investor_profile: str
    target_grade: str
    feedback: str
    grade: str
    n: int


class Feedback(BaseModel):
    grade: grades = Field(description="Risk level of the plan.")
    feedback: str = Field(description="Reasoning for the classification and how to adjust.")


def build_investment_workflow(iteration_limit: int = 5):
    """Generate a plan, grade it, and revise until it matches the target grade."""
    llm = get_llm()

    grade_pipe = ChatPromptTemplate.from_messages([
        ("system",
         "Given the investor's profile, choose exactly one risk classification from: "
         "ultra-conservative, conservative, moderate, aggressive, high risk. Return ONLY the grade."),
        ("user", "Investor profile:\n\n{investor_profile}"),
    ]) | llm

    growth_pipe = ChatPromptTemplate.from_messages([
        ("system",
         "You are an investment advisor with a growth and innovation focus. Produce a "
         "forward-looking plan that favours disruptive technology and long-term growth, "
         "accepting short-term volatility. Respond with a concise plan in paragraph form."),
        ("human", "Investor profile:\n\n{investor_profile}"),
    ]) | llm

    balanced_pipe = ChatPromptTemplate.from_messages([
        ("system",
         "You are an investment advisor applying risk-parity principles: diversify across "
         "economic regimes, weight by volatility, and account for inflation.\n\n"
         "Adapt to the feedback you are given:\n"
         "- too conservative -> add growth exposure\n"
         "- too aggressive -> add defensive assets\n\n"
         "Respond with a concise plan in paragraph form."),
        ("human",
         "Investor profile:\n\n{investor_profile}\n\n"
         "Current grade: {grade}\nTarget grade: {target_grade}\n\n"
         "Previous plan:\n{investment_plan}\n\nEvaluator feedback:\n{feedback}"),
    ]) | llm

    evaluator_pipe = ChatPromptTemplate.from_messages([
        ("system",
         "You are an investment risk evaluator applying a value-investing philosophy that "
         "emphasises capital preservation and sound fundamentals. Grade the plan's risk "
         "level and explain your reasoning."),
        ("human",
         "Investor profile:\n\n{investor_profile}\n\nProposed plan:\n{investment_plan}"),
    ]) | llm.with_structured_output(Feedback)

    def determine_target_grade(state: InvestState):
        """Pick the risk grade the plan should aim for."""
        return {"target_grade": grade_pipe.invoke(
            {"investor_profile": state["investor_profile"]}
        ).content.strip().lower()}

    def investment_plan_generator(state: InvestState) -> dict:
        """First pass uses the profile alone; later passes also use the feedback."""
        if state.get("feedback"):
            response = balanced_pipe.invoke({
                "investor_profile": state["investor_profile"],
                "grade": state.get("grade", ""),
                "target_grade": state.get("target_grade", ""),
                "investment_plan": state.get("investment_plan", ""),
                "feedback": state["feedback"],
            })
        else:
            response = growth_pipe.invoke({"investor_profile": state["investor_profile"]})
        return {"investment_plan": response.content}

    def evaluate_plan(state: InvestState):
        """Grade the current plan and count the iteration."""
        result = evaluator_pipe.invoke({
            "investment_plan": state["investment_plan"],
            "investor_profile": state["investor_profile"],
        })
        return {"grade": result.grade, "feedback": result.feedback, "n": state.get("n", 0) + 1}

    def route_investment(state: InvestState) -> str:
        """Accept on a match, or when the iteration cap is reached; otherwise revise."""
        if state.get("grade") == state.get("target_grade"):
            return "Accepted"
        if state.get("n", 0) >= iteration_limit:
            return "Accepted"   # stop rather than loop forever
        return "Rejected + Feedback"

    builder = StateGraph(InvestState)
    builder.add_node("determine_target_grade", determine_target_grade)
    builder.add_node("investment_plan_generator", investment_plan_generator)
    builder.add_node("evaluate_plan", evaluate_plan)
    builder.add_edge(START, "determine_target_grade")
    builder.add_edge("determine_target_grade", "investment_plan_generator")
    builder.add_edge("investment_plan_generator", "evaluate_plan")
    builder.add_conditional_edges(
        "evaluate_plan",
        route_investment,
        {"Accepted": END, "Rejected + Feedback": "investment_plan_generator"},
    )
    return builder.compile()
