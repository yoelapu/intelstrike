"""
config.py
=========
IntelStrike - Centralized Configuration

All pipeline settings live here. Edit this file before each engagement.
No other files need to be modified for a new engagement run.
"""

from __future__ import annotations

# -- Engagement Configuration --------------------------------------------------

ENGAGEMENT = {
    "client_industry":  "Financial Services",           # e.g. Healthcare, Retail, Tech
    "client_geography": "Latin America",                # e.g. United States, Europe
    "tech_stack":       ["WordPress", "AWS", "MySQL"],  # known technologies
    "scope_type":       "web application",              # web application / infrastructure / both
    "scope_focus":      "initial access, authentication bypass, data exfiltration",  # key objectives to prioritize
    "engagement_days":  10,                             # duration in days
}

# -- Output Configuration ------------------------------------------------------

OUTPUT_FILE = "intelstrike_report.md"

# -- LLM Configuration ---------------------------------------------------------
#
# Select your preferred LLM provider by setting LLM_PROVIDER and LLM_MODEL.
# Make sure the corresponding API key environment variable is set.
#
# Supported providers and example models:
#
#   Provider      | LLM_PROVIDER    | Example LLM_MODEL              | Env Variable
#   --------------|-----------------|--------------------------------|---------------------------
#   Anthropic     | "anthropic"     | "claude-sonnet-4-5"            | ANTHROPIC_API_KEY
#   OpenAI        | "openai"        | "gpt-4o"                       | OPENAI_API_KEY
#   Google Gemini | "google"        | "gemini/gemini-1.5-pro"        | GOOGLE_API_KEY
#   Groq          | "groq"          | "groq/llama-3.1-70b-versatile" | GROQ_API_KEY
#   Ollama        | "ollama"        | "ollama/llama3.2"              | (no key needed)
#   Azure OpenAI  | "azure"         | "azure/gpt-4o"                 | AZURE_API_KEY + AZURE_API_BASE
#   AWS Bedrock   | "bedrock"       | "bedrock/anthropic.claude-..."  | AWS credentials
#
# CrewAI uses LiteLLM under the hood, so any OpenAI-compatible endpoint works.
# Full list: https://docs.litellm.ai/docs/providers

LLM_PROVIDER = "anthropic"
LLM_MODEL    = "claude-sonnet-4-5"

# -- Agent Settings ------------------------------------------------------------

LLM_MAX_ITER = 3       # Max iterations per agent before stopping
VERBOSE      = True    # Set to False to reduce console output

# -- Search Configuration ------------------------------------------------------

# Tavily search settings
# Get your free API key at https://tavily.com (free tier: 1,000 calls/month)
SEARCH_MAX_RESULTS = 3    # Results per query - 3 is sufficient for focused CTI research
