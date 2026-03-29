"""
tasks.py
========
IntelStrike - Task Definitions

Tasks are built dynamically using the engagement context passed from main.py.
Each task receives context from the previous one via CrewAI's context mechanism.
"""

from __future__ import annotations

from crewai import Task
from agents import threat_profiler, ttp_extractor, test_case_builder


def build_tasks(engagement: dict, output_file: str) -> list[Task]:
    """
    Build the three pipeline tasks using the engagement context.

    Args:
        engagement: dict with client_industry, client_geography,
                    tech_stack, scope_type, scope_focus, engagement_days
        output_file: path where the final Markdown report will be saved

    Returns:
        List of Task objects in execution order
    """

    stack  = ", ".join(engagement["tech_stack"])
    focus  = engagement.get("scope_focus", "general security testing")

    # ── Task 1: Threat Profiling ──────────────────────────────────────────────

    task_threat_profile = Task(
        description=f"""
        Identify the 2-3 most relevant threat actor groups targeting organizations
        with the following profile:

        - Industry:   {engagement['client_industry']}
        - Geography:  {engagement['client_geography']}
        - Tech Stack: {stack}
        - Scope:      {engagement['scope_type']}

        For each threat group provide:
        1. Group name and MITRE ATT&CK ID (e.g., APT41 / G0096)
        2. Why they are relevant to this client profile
        3. Primary objectives (espionage, financial gain, disruption)
        4. Known targeting of the specific tech stack if documented
        5. Most recent documented activity (last 12-24 months if available)

        Search MITRE ATT&CK, public threat intelligence reports, and security
        vendor advisories. Prioritize groups with documented activity against
        this industry and tech stack combination.
        """,
        expected_output="""
        A structured threat profile with 2-3 relevant threat actor groups, each with:
        - Group name, ATT&CK ID, and relevance justification
        - Primary objectives and targeting patterns
        - Known activity against the client's tech stack
        - Recent campaign activity summary
        """,
        agent=threat_profiler,
    )

    # ── Task 2: TTP Extraction ────────────────────────────────────────────────

    task_ttp_extraction = Task(
        description=f"""
        Based on the threat groups identified in the previous task, extract and
        filter the most relevant TTPs for a {engagement['scope_type']} penetration
        test against a {stack} stack.

        Prioritize TTPs aligned with the following engagement focus: {focus}

        Cover the following tactic areas:
        1. Initial Access (TA0001) - techniques applicable to the identified scope and stack
        2. Execution (TA0002) - techniques viable via the identified scope and stack
        3. Persistence (TA0003) - post-exploitation persistence relevant to the stack
        4. Credential Access (TA0006) - techniques applicable to the identified stack
        5. Collection / Exfiltration - what the threat actors typically target

        For each TTP:
        - ATT&CK Technique ID and Name
        - Tactic
        - How the threat group uses this technique (specific to stack if documented)
        - Viability assessment for {stack} environments
        - Priority: HIGH / MEDIUM / LOW based on documented exploitation frequency

        Filter out TTPs that are NOT applicable to {engagement['scope_type']} testing
        or the identified tech stack. Quality over quantity - a focused list of
        10-15 high-relevance TTPs is better than an exhaustive one.
        """,
        expected_output="""
        A filtered, prioritized table of 10-15 TTPs with:
        - ATT&CK ID, Name, Tactic
        - Threat group usage notes
        - Stack applicability assessment
        - Priority level (HIGH/MEDIUM/LOW)
        """,
        agent=ttp_extractor,
        context=[task_threat_profile],
    )

    # ── Task 3: Test Case Generation ──────────────────────────────────────────

    task_test_cases = Task(
        description=f"""
        Transform the extracted TTPs into an actionable penetration testing
        checklist for a {engagement['engagement_days']}-day {engagement['scope_type']}
        engagement against {stack}.

        The engagement focus is: {focus}
        Ensure test cases directly address this focus before covering lower-priority areas.

        For each HIGH and MEDIUM priority TTP, create a test case with:
        - [ ] Checkbox format for execution tracking
        - ATT&CK Technique ID and Name
        - Preconditions required
        - Step-by-step testing approach (concise, 3-5 steps)
        - Relevant tools or payloads
        - Success criteria (what does a confirmed finding look like)
        - Effort estimate: LOW / MEDIUM / HIGH

        Then provide:
        1. TOP 5 QUICK WINS - highest impact, lowest effort test cases to
           prioritize in the first 2 days of the engagement
        2. THREAT NARRATIVE - a 2-paragraph summary of how the identified threat
           actors would chain these TTPs in a real attack against this client,
           to use as context when reporting findings

        Format everything in clean Markdown. Use headers, tables where appropriate,
        and checkboxes for the test cases. This document will be used directly
        during the pentest engagement.
        """,
        expected_output="""
        A complete Markdown document containing:
        1. Executive Summary - threat context for this engagement
        2. Threat Actor Profiles - brief summary of relevant groups
        3. Prioritized TTP Table - filtered and scored
        4. Actionable Test Cases - checkbox format with steps, tools, criteria
        5. Top 5 Quick Wins - highest impact/lowest effort
        6. Threat Narrative - attack chain story for reporting context
        """,
        agent=test_case_builder,
        context=[task_threat_profile, task_ttp_extraction],
        output_file=output_file,
    )

    return [task_threat_profile, task_ttp_extraction, task_test_cases]
