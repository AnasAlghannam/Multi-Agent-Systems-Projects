"""Shared LLM factory.

All three agents talk to the same provider through this module, so switching
models or providers is a one-file change. Credentials come from a .env file at
the project root (see .env.example) - nothing is hard-coded.
"""

import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

# Search upward from the working directory so the app finds .env whether it is
# launched from the project root or a subdirectory.
load_dotenv(find_dotenv(usecwd=True))

# Default model. Override per environment with DOCCHAT_MODEL in .env.
DEFAULT_MODEL = os.environ.get("DOCCHAT_MODEL", "llama-3.3-70b-versatile")


def _resolve_provider():
    """Return (api_key, base_url, model) for whichever provider is configured.

    Groq and OpenRouter both speak the OpenAI protocol, so switching is just a
    base URL, key and model id. OpenRouter wins when its key is set - handy when
    Groq's quota runs out or you need a model it does not host.
    """
    if os.environ.get("OPENROUTER_API_KEY"):
        return (
            os.environ["OPENROUTER_API_KEY"],
            "https://openrouter.ai/api/v1",
            os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct"),
        )
    if os.environ.get("GROQ_API_KEY"):
        return (
            os.environ["GROQ_API_KEY"],
            "https://api.groq.com/openai/v1",
            DEFAULT_MODEL,
        )
    raise RuntimeError(
        "No model provider configured. Set GROQ_API_KEY or OPENROUTER_API_KEY "
        "in your .env file."
    )


def get_callbacks() -> list:
    """Return Langfuse callbacks if configured, otherwise an empty list.

    Tracing is optional: with no credentials the list is empty and nothing
    about the run changes.
    """
    if not os.environ.get("LANGFUSE_PUBLIC_KEY"):
        return []
    try:
        from langfuse.langchain import CallbackHandler
        return [CallbackHandler()]
    except Exception as e:
        # Say why rather than disabling tracing silently - a quiet failure here
        # is exactly the kind of thing tracing is meant to prevent.
        print(f"[tracing] Langfuse disabled: {e}")
        return []


def get_llm(temperature: float = 0.0, max_tokens: int = 512, model: str | None = None) -> ChatOpenAI:
    """Return a configured chat model.

    :param temperature: 0 for deterministic output, higher for more variation
    :param max_tokens: cap on response length
    :param model: override the default model id
    :raises RuntimeError: if GROQ_API_KEY is missing, with a pointer to the fix
    """
    api_key, base_url, resolved = _resolve_provider()
    return ChatOpenAI(
        model=model or resolved,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        callbacks=get_callbacks(),
    )


def complete(llm: ChatOpenAI, prompt: str) -> str:
    """Send a single prompt and return the response text.

    Wraps the call so agents don't each repeat the message-shaping and the
    empty/failed-response handling.
    """
    response = llm.invoke(prompt)
    return (response.content or "").strip()
