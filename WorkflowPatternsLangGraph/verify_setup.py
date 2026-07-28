#!/usr/bin/env python3
"""Run each workflow once against the live model to confirm the setup works.

    python verify_setup.py
"""

import sys


def main() -> int:
    print("Workflow patterns verification")
    print("=" * 60)

    try:
        from workflows import (
            get_llm,
            build_chain_workflow,
            build_routing_workflow,
            build_parallel_workflow,
            build_multi_agent_workflow,
        )
    except ImportError as e:
        print(f"FAILED: could not import workflows: {e}")
        return 1

    # 1 - key and connectivity
    print("\n[1/5] Checking API key and model...")
    try:
        reply = get_llm().invoke("Reply with exactly: OK").content.strip()
    except RuntimeError as e:
        print(f"FAILED: {e}")
        return 1
    except Exception as e:
        print(f"FAILED: model call failed: {e}")
        return 1
    print(f"      OK - model replied {reply[:20]!r}")

    # 2 - prompt chaining
    print("\n[2/5] Prompt chaining...")
    try:
        r = build_chain_workflow().invoke({
            "job_description": "Data scientist with Python and SQL experience.",
            "resume_summary": "",
            "cover_letter": "",
        })
        assert r["resume_summary"] and r["cover_letter"]
    except Exception as e:
        print(f"FAILED: {e}")
        return 1
    print(f"      OK - summary {len(r['resume_summary'])} chars, "
          f"letter {len(r['cover_letter'])} chars")

    # 3 - routing (both branches)
    print("\n[3/5] Routing...")
    try:
        graph = build_routing_workflow()
        a = graph.invoke({"user_input": "Translate to French: good morning",
                          "task_type": "", "output": ""})
        b = graph.invoke({"user_input": "Summarize: the panels produced more energy after cleaning.",
                          "task_type": "", "output": ""})
        assert a["output"] and b["output"]
    except Exception as e:
        print(f"FAILED: {e}")
        return 1
    print(f"      OK - branches chosen: {a['task_type']!r}, {b['task_type']!r}")

    # 4 - parallelization
    print("\n[4/5] Parallelization...")
    try:
        r = build_parallel_workflow().invoke({
            "text": "The train arrives at nine.",
            "french": "", "spanish": "", "japanese": "", "combined_output": "",
        })
        assert r["french"] and r["spanish"] and r["japanese"]
    except Exception as e:
        print(f"FAILED: {e}")
        return 1
    print("      OK - all three translations returned")

    # 5 - multi-agent routing across every branch
    print("\n[5/5] Multi-agent routing...")
    cases = [
        "I need a ride from downtown to the airport at 3pm",
        "I want to order 2 large pepperoni pizzas for delivery",
        "I need milk, bread, eggs and vegetables for the week",
        "What's the weather like today?",
    ]
    try:
        graph = build_multi_agent_workflow()
        routed = []
        for text in cases:
            out = graph.invoke({"user_input": text, "task_type": "", "output": ""})
            assert out["output"], f"no output for: {text}"
            routed.append(out["task_type"])
    except Exception as e:
        print(f"FAILED: {e}")
        return 1
    for text, handler in zip(cases, routed):
        print(f"      {handler:<20} <- {text[:45]}")

    print("\n" + "=" * 60)
    print("All checks passed. Start the UI with:  python app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
