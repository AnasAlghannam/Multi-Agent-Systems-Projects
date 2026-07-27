"""Shared LLM factory.

All three agents talk to the same provider through this module, so switching
models or providers is a one-file change. Credentials come from a .env file at
the project root (see .env.example) - nothing is hard-coded.
"""

import os

from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq

# Search upward from the working directory so the app finds .env whether it is
# launched from the project root or a subdirectory.
load_dotenv(find_dotenv(usecwd=True))

# Default model. Override per environment with DOCCHAT_MODEL in .env.
DEFAULT_MODEL = os.environ.get("DOCCHAT_MODEL", "llama-3.3-70b-versatile")


def get_llm(temperature: float = 0.0, max_tokens: int = 512, model: str | None = None) -> ChatGroq:
    """Return a configured chat model.

    :param temperature: 0 for deterministic output, higher for more variation
    :param max_tokens: cap on response length
    :param model: override the default model id
    :raises RuntimeError: if GROQ_API_KEY is missing, with a pointer to the fix
    """
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(get one free at https://console.groq.com/keys)."
        )

    return ChatGroq(
        model=model or DEFAULT_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def complete(llm: ChatGroq, prompt: str) -> str:
    """Send a single prompt and return the response text.

    Wraps the call so agents don't each repeat the message-shaping and the
    empty/failed-response handling.
    """
    response = llm.invoke(prompt)
    return (response.content or "").strip()
