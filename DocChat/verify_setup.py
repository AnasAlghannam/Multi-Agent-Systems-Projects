#!/usr/bin/env python3
"""End-to-end check that DocChat is correctly installed and configured.

Runs each layer in order and reports which one fails, so a broken setup points
at its own cause. Exits non-zero on the first failure.

    python verify_setup.py
"""

import sys
from pathlib import Path
from types import SimpleNamespace

SAMPLE = Path(__file__).parent / "examples" / "sample-solar-report.md"
QUESTION = (
    "What is the efficiency range of monocrystalline panels, "
    "and how long is the typical warranty?"
)


def step(n: int, label: str) -> None:
    print(f"\n[{n}/5] {label}")


def fail(message: str) -> "NoReturn":  # type: ignore[valid-type]
    print(f"\nFAILED: {message}")
    sys.exit(1)


def main() -> int:
    print("DocChat setup verification")
    print("=" * 60)

    # 1 - dependencies import
    step(1, "Importing dependencies...")
    try:
        from document_processor.file_handler import DocumentProcessor
        from retriever.builder import RetrieverBuilder
        from agents.workflow import AgentWorkflow
        from utils.llm import get_llm, complete
    except ImportError as e:
        fail(f"could not import project modules: {e}\n"
             f"        Did you install requirements into the active environment?")
    print("      OK - all modules imported")

    # 2 - API key present and the model responds
    step(2, "Checking the API key and model connectivity...")
    try:
        reply = complete(get_llm(max_tokens=10), "Reply with exactly: OK")
    except RuntimeError as e:
        fail(str(e))
    except Exception as e:
        fail(f"model call failed: {e}")
    print(f"      OK - model replied: {reply[:40]!r}")

    # 3 - document parsing
    step(3, f"Parsing the sample document ({SAMPLE.name})...")
    if not SAMPLE.exists():
        fail(f"sample document missing at {SAMPLE}")
    try:
        processor = DocumentProcessor()
        # DocumentProcessor expects objects with a .name attribute, matching the
        # file objects Gradio hands over from an upload.
        chunks = processor.process([SimpleNamespace(name=str(SAMPLE))])
    except Exception as e:
        fail(f"document processing failed: {e}")
    if not chunks:
        fail("document produced no chunks - parsing likely failed")
    print(f"      OK - {len(chunks)} chunk(s) extracted")

    # 4 - embeddings + hybrid retriever
    step(4, "Building the hybrid retriever (downloads the embedding model on first run)...")
    try:
        retriever = RetrieverBuilder().build_hybrid_retriever(chunks)
        hits = retriever.invoke(QUESTION)
    except Exception as e:
        fail(f"retriever construction failed: {e}")
    if not hits:
        fail("retriever returned no documents")
    print(f"      OK - retrieved {len(hits)} passage(s)")

    # 5 - the three-agent workflow
    step(5, "Running the multi-agent workflow...")
    try:
        result = AgentWorkflow().full_pipeline(question=QUESTION, retriever=retriever)
    except Exception as e:
        fail(f"workflow failed: {e}")

    answer = (result.get("draft_answer") or "").strip()
    report = (result.get("verification_report") or "").strip()
    if not answer:
        fail("workflow returned an empty answer")
    print("      OK - workflow completed")

    print("\n" + "=" * 60)
    print("QUESTION:\n  " + QUESTION)
    print("\nANSWER:")
    for line in answer.splitlines():
        print("  " + line)
    print("\nVERIFICATION REPORT:")
    for line in (report or "(none returned)").splitlines():
        print("  " + line)

    print("\n" + "=" * 60)
    print("All checks passed. Start the app with:  python app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
