#!/usr/bin/env python3
"""Run both workflows once against the live model to confirm the setup works.

    python verify_setup.py
"""

import sys


def main() -> int:
    print("Orchestration & evaluation verification")
    print("=" * 60)

    try:
        from workflows import get_llm, build_meal_workflow, build_investment_workflow
    except ImportError as e:
        print(f"FAILED: could not import workflows: {e}")
        return 1

    print("\n[1/3] Checking API key and model...")
    try:
        reply = get_llm().invoke("Reply with exactly: OK").content.strip()
    except RuntimeError as e:
        print(f"FAILED: {e}")
        return 1
    except Exception as e:
        print(f"FAILED: model call failed: {e}")
        return 1
    print(f"      OK - model replied {reply[:20]!r}")

    print("\n[2/3] Orchestrator-worker (parallel meal planning)...")
    try:
        r = build_meal_workflow().invoke({
            "meals": "banana smoothie, carrot cake",
            "sections": [], "completed_menu": [], "final_meal_guide": "",
        })
        assert r["sections"], "planner produced no dishes"
        assert r["final_meal_guide"], "synthesizer produced no guide"
    except Exception as e:
        print(f"FAILED: {e}")
        return 1
    print(f"      OK - {len(r['sections'])} dish(es) planned, "
          f"{len(r['completed_menu'])} section(s) written in parallel")
    for d in r["sections"]:
        print(f"         - {d.name} ({d.location})")

    print("\n[3/3] Reflection loop (investment plan)...")
    try:
        r = build_investment_workflow(iteration_limit=3).invoke({
            "investor_profile": "I am 63 and retiring in two years. Preserving capital matters most.",
            "investment_plan": "", "target_grade": "", "feedback": "", "grade": "", "n": 0,
        })
        assert r["investment_plan"], "no plan produced"
        assert r["grade"], "no grade assigned"
    except Exception as e:
        print(f"FAILED: {e}")
        return 1
    print(f"      OK - target={r['target_grade']!r} final={r['grade']!r} "
          f"after {r['n']} iteration(s), plan {len(r['investment_plan'])} chars")

    print("\n" + "=" * 60)
    print("All checks passed. Start the UI with:  python app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
