"""
main.py
=======
IntelStrike - Entry Point

Usage:
  pip install -r requirements.txt

  export ANTHROPIC_API_KEY="your-key"   # or the key for your chosen provider
  export TAVILY_API_KEY="your-key"

  python main.py
  python main.py --dry-run              # validate config without running

"""

from __future__ import annotations

import argparse
import os
import sys

from crewai import Crew, Process

from agents import threat_profiler, ttp_extractor, test_case_builder
from tasks import build_tasks
from config import ENGAGEMENT, LLM_PROVIDER, OUTPUT_FILE, VERBOSE


# -- Validation ----------------------------------------------------------------

PROVIDER_KEY_MAP: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai":    "OPENAI_API_KEY",
    "google":    "GOOGLE_API_KEY",
    "groq":      "GROQ_API_KEY",
    "azure":     "AZURE_API_KEY",
}


def validate_engagement(engagement: dict) -> None:
    """Validate that all required engagement fields are present and non-empty."""
    required = ["client_industry", "client_geography", "tech_stack", "scope_type", "engagement_days"]
    missing = [k for k in required if k not in engagement]
    if missing:
        raise ValueError(f"Missing required engagement fields: {missing}")
    if not engagement["tech_stack"]:
        raise ValueError("tech_stack cannot be empty")


def check_api_keys() -> None:
    """Verify that required API keys are set as environment variables."""
    required_key = PROVIDER_KEY_MAP.get(LLM_PROVIDER)
    if required_key and not os.getenv(required_key):
        raise EnvironmentError(
            f"Missing {required_key} for provider '{LLM_PROVIDER}'. "
            f"Run: export {required_key}=your-key"
        )
    if not os.getenv("TAVILY_API_KEY"):
        raise EnvironmentError(
            "Missing TAVILY_API_KEY. "
            "Get a free key at https://tavily.com and run: export TAVILY_API_KEY=your-key"
        )


# -- Pipeline Execution --------------------------------------------------------

def main() -> None:
    """Run the CTI-informed pentesting pipeline."""

    parser = argparse.ArgumentParser(description="IntelStrike")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and API keys without running the pipeline",
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  IntelStrike")
    print("=" * 60)
    print(f"\n  Engagement Profile:")
    print(f"    Industry   : {ENGAGEMENT['client_industry']}")
    print(f"    Geography  : {ENGAGEMENT['client_geography']}")
    print(f"    Tech Stack : {', '.join(ENGAGEMENT['tech_stack'])}")
    print(f"    Scope      : {ENGAGEMENT['scope_type']}")
    print(f"    Focus      : {ENGAGEMENT.get('scope_focus', 'general security testing')}")
    print(f"    Duration   : {ENGAGEMENT['engagement_days']} days")
    print(f"\n  Output      : {OUTPUT_FILE}")
    print("=" * 60 + "\n")

    validate_engagement(ENGAGEMENT)
    check_api_keys()

    if args.dry_run:
        print("  Dry run complete - config and API keys validated.")
        print("=" * 60 + "\n")
        return

    tasks = build_tasks(ENGAGEMENT, OUTPUT_FILE)

    crew = Crew(
        agents=[threat_profiler, ttp_extractor, test_case_builder],
        tasks=tasks,
        process=Process.sequential,
        verbose=VERBOSE,
    )

    try:
        crew.kickoff()
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(f"  Pipeline complete.")
    print(f"  Report saved to: {OUTPUT_FILE}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Interrupted]")
        sys.exit(130)
