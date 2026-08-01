"""Shared LLM configuration for the AG2 examples.

AG2 talks to any OpenAI-compatible endpoint, so pointing it at Groq is just a
matter of `base_url` and `api_type`. Keys come from a .env file - nothing is
hard-coded.
"""

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

MODEL = os.environ.get("AG2_MODEL", "llama-3.3-70b-versatile")
BASE_URL = os.environ.get("AG2_BASE_URL", "https://api.groq.com/openai/v1")


def get_llm_config(temperature: float = 0.2) -> dict:
    """Return the `llm_config` dict every agent in these notebooks uses."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com/keys)."
        )

    return {
        "config_list": [{
            "model": MODEL,
            "api_key": api_key,
            "base_url": BASE_URL,
            # Groq speaks the OpenAI protocol, so AG2's openai client works as-is.
            "api_type": "openai",
        }],
        "temperature": temperature,
    }


# Convenience for notebook cells that just want the default.
llm_config = get_llm_config()
