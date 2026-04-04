#!/usr/bin/env python3
"""
Autoresearch — Karpathy-style autonomous research engine.

Iteratively searches, analyzes, and synthesizes web research on any topic.
Each iteration: identify gaps → search → synthesize → evaluate → commit if improved.

Usage:
    python autoresearch.py "What are the best elevator compliance solutions in EU?"
    python autoresearch.py "AI marketing trends 2026" --max-iterations 20
    python autoresearch.py "B2B SaaS interview tool competitors" --output report.md
    python autoresearch.py "topic" --model google/gemini-2.5-flash-preview

Requires:
    - OPENROUTER_API_KEY in environment (for LLM calls)
    - Optional: SEARCHAPI_API_KEY (for Google search; falls back to DuckDuckGo)
"""

import argparse
import logging
import sys
import os

# Ensure project directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from researcher import run_loop


def main():
    parser = argparse.ArgumentParser(
        description="Autoresearch — iterative web research engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "EU elevator compliance regulations 2026"
  %(prog)s "competitor analysis: Typeform vs SurveyMonkey" --max-iterations 15
  %(prog)s "AI agents in marketing automation" --model google/gemini-2.5-flash-preview --threshold 70
  %(prog)s "React Server Components best practices" --output rsc-research.md
        """,
    )

    parser.add_argument(
        "topic",
        help="Research topic (natural language question or phrase)",
    )
    parser.add_argument(
        "--max-iterations", "-n",
        type=int,
        default=10,
        help="Maximum number of research iterations (default: 10)",
    )
    parser.add_argument(
        "--output", "-o",
        default="research.md",
        help="Output file for research document (default: research.md)",
    )
    parser.add_argument(
        "--model", "-m",
        default="anthropic/claude-sonnet-4-6",
        help="OpenRouter model ID (default: anthropic/claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--threshold", "-t",
        type=int,
        default=80,
        help="Quality score threshold to stop (0-100, default: 80)",
    )
    parser.add_argument(
        "--max-cost",
        type=float,
        default=2.0,
        help="Maximum estimated API cost in USD before stopping (default: $2.00)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Project directory (default: current directory)",
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Validate API key
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY environment variable is required.", file=sys.stderr)
        print("Set it with: export OPENROUTER_API_KEY='sk-or-v1-...'", file=sys.stderr)
        sys.exit(1)

    # Run the research loop
    try:
        summary = run_loop(
            topic=args.topic,
            max_iterations=args.max_iterations,
            threshold=args.threshold,
            output=args.output,
            model=args.model,
            max_cost=args.max_cost,
            project_dir=args.project_dir or os.getcwd(),
        )
        sys.exit(0 if summary["final_score"] > 0 else 1)
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
