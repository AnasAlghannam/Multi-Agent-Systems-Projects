#!/usr/bin/env python3
"""Check that NourishBot is installed and configured correctly.

    python verify_setup.py
"""

import sys


def main() -> int:
    print("NourishBot setup verification")
    print("=" * 60)

    print("\n[1/4] Importing modules...")
    try:
        from src.llm import chat, vision_available, TEXT_MODEL, VISION_MODEL
        from src.crew import NourishBotRecipeCrew, NourishBotAnalysisCrew
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")
        return 1
    print("      OK - crew and model modules imported")

    print("\n[2/4] Checking the API key and text model...")
    try:
        reply = chat("Reply with exactly: OK", max_tokens=10)
    except RuntimeError as e:
        print(f"FAILED: {e}")
        return 1
    except Exception as e:
        print(f"FAILED: model call failed: {e}")
        return 1
    print(f"      OK - {TEXT_MODEL} replied {reply[:20]!r}")

    print("\n[3/4] Checking vision support...")
    if vision_available():
        print(f"      Vision model configured: {VISION_MODEL}")
        print("      Image upload will be used for ingredient detection.")
    else:
        print("      No vision model configured (NOURISH_VISION_MODEL is blank).")
        print("      The UI will ask for a typed ingredient list instead - the other")
        print("      three agents run unchanged.")

    print("\n[4/4] Building the crews...")
    ingredients = "tomato, mozzarella, basil, olive oil"
    try:
        recipe_crew = NourishBotRecipeCrew(
            image_data=ingredients, dietary_restrictions="vegetarian"
        )
        analysis_crew = NourishBotAnalysisCrew(image_data=ingredients)
        recipe_crew.crew()
        analysis_crew.crew()
    except Exception as e:
        print(f"FAILED: could not build crews: {type(e).__name__}: {e}")
        return 1
    print("      OK - both crews assembled")

    print("\n" + "=" * 60)
    print("All checks passed. Start the UI with:  python app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
