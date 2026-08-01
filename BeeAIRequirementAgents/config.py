"""Shared model configuration for the BeeAI examples.

Every example builds its model through `get_llm()`, so switching provider or
model is a one-file change. Credentials come from a .env file at the project
root (see .env.example) - nothing is hard-coded.
"""

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from beeai_framework.backend import ChatModel, ChatModelParameters

# BeeAI addresses models as "provider:model". It ships a groq provider, which
# reads GROQ_API_KEY from the environment.
PROVIDER = os.environ.get("BEEAI_PROVIDER", "groq")
MODEL = os.environ.get("BEEAI_MODEL", "llama-3.3-70b-versatile")


def get_llm(temperature: float = 0.0) -> ChatModel:
    """Return the chat model used by every example."""
    if PROVIDER == "groq" and not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com/keys)."
        )

    return ChatModel.from_name(
        f"{PROVIDER}:{MODEL}",
        ChatModelParameters(temperature=temperature),
    )
