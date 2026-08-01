#!/usr/bin/env python3
"""Check the BeeAI setup, then optionally run every example.

    python verify_setup.py            # quick check: key, model, imports
    python verify_setup.py --all      # also run each example end to end (slow)

Examples that wait for input (the permission prompts in 09 and 11) are skipped
by --all; run those two by hand.
"""

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).parent / "examples"
# These block on an interactive permission prompt, so they can't run unattended.
INTERACTIVE = {"09_permissions_and_safety.py", "11_multi_agent_travel_planner.py"}


async def check_model() -> str:
    from beeai_framework.backend import UserMessage
    from config import get_llm, PROVIDER, MODEL

    llm = get_llm()
    response = await llm.run([UserMessage(content="Reply with exactly: OK")])
    return f"{PROVIDER}:{MODEL} replied {response.get_text_content().strip()[:20]!r}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="run every example")
    args = parser.parse_args()

    print("BeeAI setup verification")
    print("=" * 60)

    print("\n[1/3] Importing the framework...")
    try:
        import beeai_framework  # noqa: F401
        from beeai_framework.agents.requirement import RequirementAgent  # noqa: F401
    except ImportError as e:
        print(f"FAILED: {e}\n        Did you install requirements.txt into this environment?")
        return 1
    print("      OK - beeai_framework imported")

    print("\n[2/3] Checking the API key and model...")
    try:
        print(f"      OK - {asyncio.run(check_model())}")
    except RuntimeError as e:
        print(f"FAILED: {e}")
        return 1
    except Exception as e:
        print(f"FAILED: model call failed: {type(e).__name__}: {e}")
        return 1

    scripts = sorted(EXAMPLES_DIR.glob("*.py"))
    if not args.all:
        print(f"\n[3/3] Found {len(scripts)} examples. Run one with:")
        print(f"      python examples/{scripts[0].name}")
        print("      (pass --all to run them all)")
        print("\n" + "=" * 60)
        print("Setup looks good.")
        return 0

    print(f"\n[3/3] Running {len(scripts)} examples...")
    failures = []
    for script in scripts:
        if script.name in INTERACTIVE:
            print(f"      SKIP  {script.name} (waits for input; run it by hand)")
            continue
        proc = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=600,
        )
        if proc.returncode == 0:
            print(f"      OK    {script.name}")
        else:
            tail = (proc.stderr or "").strip().splitlines()
            print(f"      FAIL  {script.name}: {tail[-1][:100] if tail else 'unknown error'}")
            failures.append(script.name)

    print("\n" + "=" * 60)
    if failures:
        print(f"{len(failures)} example(s) failed: {', '.join(failures)}")
        return 1
    print("All examples ran successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
