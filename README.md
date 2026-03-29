# IntelStrike

A multi-agent AI pipeline that operationalizes Cyber Threat Intelligence (CTI) for penetration testing engagements. Built with CrewAI, Claude, and Tavily.

---

## How It Works

Three agents run sequentially, each passing context to the next:

```
[config.py]
    │
    ▼
Agent 1: Threat Profiler
    Identifies 2-3 threat groups relevant to the client's
    industry, geography, and tech stack
    │
    ▼
Agent 2: TTP Extractor
    Extracts and filters TTPs applicable to the known stack,
    mapped to MITRE ATT&CK, prioritized by exploitation frequency
    │
    ▼
Agent 3: Test Case Builder
    Translates TTPs into an actionable checklist with steps,
    tools, payloads, success criteria, and quick wins
    │
    ▼
[intelstrike_report.md]
```

### Output

A Markdown report containing:

- **Executive Summary** - threat context for the engagement
- **Threat Actor Profiles** - relevant groups and their targeting patterns
- **Prioritized TTP Table** - filtered by stack, scored by priority
- **Actionable Test Cases** - checkbox format with steps, tools, and criteria
- **Top 5 Quick Wins** - highest impact / lowest effort to tackle first
- **Threat Narrative** - attack chain story to contextualize findings in reports

---

## Project Structure

```
intelstrike/
├── .gitignore         # protects secrets and outputs from version control
├── README.md
├── requirements.txt   # dependencies
├── config.py          # only file you edit per engagement
├── agents.py          # agent definitions
├── tasks.py           # task definitions
└── main.py            # entry point
```

**config.py**
Centralized configuration for the pipeline. Contains the engagement profile (industry, geography, tech stack, scope, duration), LLM provider and model selection, output file path, and search settings. This is the only file you need to edit before running a new engagement.

**agents.py**
Defines the three AI agents used in the pipeline. Each agent has a specific role, goal, and backstory that shapes how it approaches its task. Also contains the `_build_llm()` function that dynamically constructs the LLM object based on the provider configured in `config.py`.

| Agent | Role | Responsibility |
|---|---|---|
| `threat_profiler` | Threat Intelligence Analyst | Researches and identifies relevant threat actor groups for the client profile |
| `ttp_extractor` | Offensive Security TTP Specialist | Extracts and filters TTPs from identified groups, mapped to MITRE ATT&CK |
| `test_case_builder` | Penetration Testing Lead | Translates TTPs into an actionable pentest checklist |

**tasks.py**
Defines the three tasks executed by the pipeline, built dynamically using the engagement context from `config.py`. Each task specifies what the agent must do, what output is expected, and which previous task results it has access to via CrewAI's context mechanism.

**main.py**
Entry point for the pipeline. Imports configuration, initializes the agents and tasks, assembles the CrewAI crew, and runs the pipeline. Also handles the console output that shows the engagement profile before execution starts.

---

## Setup

### Requirements

Python 3.10 or higher is required. CrewAI supports 3.10-3.12.

```bash
python3 --version  # verify your version
```

### 1. Create a virtual environment

A virtual environment is recommended on all platforms. It isolates project dependencies and avoids conflicts with system packages.

```bash
python3 -m venv venv
source venv/bin/activate      # Mac / Linux
venv\Scripts\activate         # Windows
```

You should see `(venv)` at the start of your terminal prompt confirming the environment is active.

### 2. Install dependencies

```bash
./venv/bin/pip3 install -r requirements.txt
```

### 3. Set environment variables

Set the API key for your chosen LLM provider and Tavily:

```bash
# Tavily (required for web search)
export TAVILY_API_KEY="your-key"      # https://tavily.com (free tier: 1,000 calls/month)

# Choose ONE LLM provider:
export ANTHROPIC_API_KEY="your-key"   # https://console.anthropic.com
export OPENAI_API_KEY="your-key"      # https://platform.openai.com
export GOOGLE_API_KEY="your-key"      # https://aistudio.google.com
export GROQ_API_KEY="your-key"        # https://console.groq.com (free tier available)
# Ollama: no key needed, just run: ollama pull llama3.2
```

### 4. Configure the engagement

Edit `config.py` with the client's details and your preferred LLM:

```python
# LLM provider - pick one
LLM_PROVIDER = "anthropic"          # anthropic / openai / google / groq / ollama / azure / bedrock
LLM_MODEL    = "claude-sonnet-4-5"  # model name for the selected provider

ENGAGEMENT = {
    "client_industry":  "Financial Services",
    "client_geography": "Latin America",
    "tech_stack":       ["WordPress", "AWS", "MySQL"],
    "scope_type":       "web application",
    "scope_focus":      "initial access, authentication bypass, data exfiltration",
    "engagement_days":  10,
}
```

**Provider and model examples:**

| Provider | `LLM_PROVIDER` | `LLM_MODEL` |
|---|---|---|
| Anthropic | `"anthropic"` | `"claude-sonnet-4-5"` |
| OpenAI | `"openai"` | `"gpt-4o"` |
| Google Gemini | `"google"` | `"gemini/gemini-1.5-pro"` |
| Groq | `"groq"` | `"groq/llama-3.1-70b-versatile"` |
| Ollama (local) | `"ollama"` | `"ollama/llama3.2"` |

### 5. Run the pipeline

```bash
python main.py
```

Validate config and API keys without running:
```bash
python main.py --dry-run
```

The report is saved to `intelstrike_report.md` by default. The output path can be changed in `config.py`.

---

## Configuration Reference

All settings live in `config.py`:

| Setting | Description | Default |
|---|---|---|
| `ENGAGEMENT["client_industry"]` | Client's industry vertical | `"Financial Services"` |
| `ENGAGEMENT["client_geography"]` | Client's operating geography | `"Latin America"` |
| `ENGAGEMENT["tech_stack"]` | Known technologies in scope | `["WordPress", "AWS", "MySQL"]` |
| `ENGAGEMENT["scope_type"]` | Type of engagement | `"web application"` |
| `ENGAGEMENT["scope_focus"]` | Key objectives to prioritize within the scope | `"initial access, authentication bypass, data exfiltration"` |
| `ENGAGEMENT["engagement_days"]` | Engagement duration in days | `10` |
| `OUTPUT_FILE` | Output report filename | `"intelstrike_report.md"` |
| `LLM_PROVIDER` | LLM provider to use | `"anthropic"` |
| `LLM_MODEL` | Model name for the selected provider | `"claude-sonnet-4-5"` |
| `LLM_MAX_ITER` | Max agent iterations | `3` |
| `VERBOSE` | Console output verbosity | `True` |
| `SEARCH_MAX_RESULTS` | Tavily results per query | `3` |

---

## Adapting to Different Engagement Types

The pipeline is not limited to web application testing. It works for any engagement type - the agents adapt their research and TTP selection based on `scope_type`, `scope_focus`, and `tech_stack`.

**Web Application**
```python
ENGAGEMENT = {
    "client_industry":  "Financial Services",
    "client_geography": "Latin America",
    "tech_stack":       ["WordPress", "AWS", "MySQL"],
    "scope_type":       "web application",
    "scope_focus":      "initial access, authentication bypass, data exfiltration",
    "engagement_days":  10,
}
```

**Active Directory / Internal Network**
```python
ENGAGEMENT = {
    "client_industry":  "Government",
    "client_geography": "United States",
    "tech_stack":       ["Active Directory", "Windows Server 2022", "Exchange"],
    "scope_type":       "internal network",
    "scope_focus":      "lateral movement, privilege escalation, domain compromise",
    "engagement_days":  14,
}
```

**Infrastructure / Network**
```python
ENGAGEMENT = {
    "client_industry":  "Energy",
    "client_geography": "Europe",
    "tech_stack":       ["Cisco IOS", "Windows Server", "VMware"],
    "scope_type":       "infrastructure",
    "scope_focus":      "network access, credential harvesting, persistence",
    "engagement_days":  10,
}
```

**Cloud**
```python
ENGAGEMENT = {
    "client_industry":  "Technology",
    "client_geography": "Asia Pacific",
    "tech_stack":       ["AWS", "S3", "EC2", "IAM", "Lambda"],
    "scope_type":       "cloud",
    "scope_focus":      "misconfiguration, IAM privilege escalation, data exfiltration",
    "engagement_days":  7,
}
```

---

## License

MIT - use freely, attribution appreciated.
