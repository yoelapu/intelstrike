"""
agents.py
=========
IntelStrike - Agent Definitions

Three agents working in sequence:
  1. Threat Profiler    - identifies relevant threat groups
  2. TTP Extractor      - extracts and filters relevant TTPs
  3. Test Case Builder  - translates TTPs into actionable test cases

LLM provider is configured in config.py - no changes needed here.
"""

from __future__ import annotations

from crewai import Agent, LLM
from crewai_tools import TavilySearchTool
from config import LLM_PROVIDER, LLM_MODEL, LLM_MAX_ITER, VERBOSE, SEARCH_MAX_RESULTS

# -- LLM Setup -----------------------------------------------------------------
#
# Builds the LLM object based on the provider set in config.py.
# Uses LiteLLM prefix convention for all providers.

def _build_llm() -> LLM:
    """Build LLM instance using LiteLLM prefix convention.

    If the model string already contains a slash, it is treated as fully
    qualified (e.g. "groq/llama-3.1-70b-versatile") and used as-is.
    Otherwise the provider prefix is prepended (e.g. "anthropic/claude-sonnet-4-5").
    """
    if "/" in LLM_MODEL:
        return LLM(model=LLM_MODEL)
    return LLM(model=f"{LLM_PROVIDER}/{LLM_MODEL}")


llm: LLM = _build_llm()
search_tool: TavilySearchTool = TavilySearchTool(max_results=SEARCH_MAX_RESULTS)

# -- Agent Definitions ---------------------------------------------------------

threat_profiler = Agent(
    role="Threat Intelligence Analyst",
    goal=(
        "Identify the most relevant threat actor groups targeting organizations "
        "in the client's industry and geography. Focus on groups known to target "
        "the identified scope type and tech stack."
    ),
    backstory=(
        "You are a senior threat intelligence analyst with deep expertise in "
        "attributing cyberattacks to specific threat groups. You specialize in "
        "understanding which adversaries are most likely to target specific "
        "industries, geographies, and technology stacks. You use MITRE ATT&CK "
        "and public threat intelligence reports to build accurate threat profiles."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=VERBOSE,
    max_iter=LLM_MAX_ITER,
)

ttp_extractor = Agent(
    role="Offensive Security TTP Specialist",
    goal=(
        "Extract and filter the most relevant TTPs from identified threat groups, "
        "focusing specifically on techniques applicable to the client's tech stack, "
        "scope type, and engagement focus. Map all findings to MITRE ATT&CK framework. "
        "Prioritize tactics most relevant to the engagement scope and focus areas."
    ),
    backstory=(
        "You are an offensive security specialist with extensive experience in "
        "red team operations and threat emulation. You know how to take raw threat "
        "intelligence and translate it into technically precise attack techniques "
        "that are relevant to specific technology environments. You think like an "
        "attacker and understand which TTPs are actually viable given a specific stack."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=VERBOSE,
    max_iter=LLM_MAX_ITER,
)

test_case_builder = Agent(
    role="Penetration Testing Lead",
    goal=(
        "Transform the extracted TTPs into a prioritized, actionable pentesting "
        "checklist. Each test case must include: the ATT&CK technique ID, "
        "preconditions, step-by-step test approach, example payloads or tools, "
        "and success criteria. Score each case by impact and effort to identify "
        "quick wins. Format output as clean Markdown ready to use during testing."
    ),
    backstory=(
        "You are a pentesting team lead with years of experience running web "
        "application and infrastructure assessments. You excel at translating "
        "threat intelligence into practical test cases that testers can execute "
        "efficiently within time-constrained engagements. You understand the "
        "difference between theoretical vulnerabilities and exploitable ones, "
        "and you always keep the attacker mindset - not just checking boxes."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=VERBOSE,
    max_iter=LLM_MAX_ITER,
)
