"""Model access for NourishBot.

Everything that talks to a model goes through here, so switching provider is a
one-file change.

Text generation runs on Groq. Image understanding is separate: not every Groq
account exposes a vision-capable model, so `describe_image` reports whether one
is available and the app falls back to a typed ingredient list when it is not.
"""

import base64
import os
from io import BytesIO

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from groq import Groq

TEXT_MODEL = os.environ.get("NOURISH_TEXT_MODEL", "llama-3.3-70b-versatile")
# Vision-capable Groq models (for example llama-4-scout) are not on every
# account. Set NOURISH_VISION_MODEL if yours has one.
VISION_MODEL = os.environ.get("NOURISH_VISION_MODEL", "")


class VisionUnavailable(RuntimeError):
    """Raised when no vision model is configured or the call is rejected."""


def _client() -> Groq:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "(free at https://console.groq.com/keys)."
        )
    return Groq(api_key=key)


def chat(prompt: str, max_tokens: int = 500, temperature: float = 0.2) -> str:
    """Send a text prompt and return the reply."""
    response = _client().chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return (response.choices[0].message.content or "").strip()


def _encode_image(image_input: str) -> str:
    """Read a local path or URL and return base64-encoded bytes."""
    if image_input.startswith("http"):
        response = requests.get(image_input, timeout=30)
        response.raise_for_status()
        data = BytesIO(response.content)
    else:
        if not os.path.isfile(image_input):
            raise FileNotFoundError(f"No file found at path: {image_input}")
        with open(image_input, "rb") as f:
            data = BytesIO(f.read())
    return base64.b64encode(data.read()).decode("utf-8")


def vision_available() -> bool:
    """True when a vision model has been configured."""
    return bool(VISION_MODEL)


def describe_image(image_input: str, prompt: str, max_tokens: int = 300) -> str:
    """Ask a vision model about an image.

    :raises VisionUnavailable: if no vision model is set, or the provider
        rejects multimodal input - the caller should fall back to asking the
        user for the ingredients directly.
    """
    if not VISION_MODEL:
        raise VisionUnavailable(
            "No vision model configured. Set NOURISH_VISION_MODEL in .env to a "
            "vision-capable model your account can use, or enter ingredients manually."
        )

    encoded = _encode_image(image_input)
    try:
        response = _client().chat.completions.create(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": "data:image/jpeg;base64," + encoded}},
                ],
            }],
            max_tokens=max_tokens,
        )
    except Exception as e:
        raise VisionUnavailable(
            f"Vision model {VISION_MODEL!r} could not process the image: {e}"
        ) from e

    return (response.choices[0].message.content or "").strip()
