# MajorProj: Agentic Customer Review Analysis

MajorProj is an advanced, agentic-architecture-powered project that automates the analysis of customer reviews using a multi-agent system built atop [crewAI](https://crewai.com). Designed for flexibility and extensibility, MajorProj enables deep, feature-based sentiment analysis, efficient review scraping, and collaborative research generation, all orchestrated through autonomous, specialized AI agents.

---

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Agentic Architecture](#agentic-architecture)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Configuration](#configuration)
- [Technologies Used](#technologies-used)
- [Support](#support)

---

## Features

- **Multi-Agent AI Workflow**: Employs autonomous agents for orchestrated review scraping, feature extraction, and analysis.
- **Amazon Review Scraping**: Automated extraction of customer reviews from Amazon product pages, with robust CSV export.
- **Feature Extraction**: Identifies and extracts key product features from reviews (e.g., Comfort, Durability, Battery Life, etc.).
- **Sentiment Analysis & Reporting**: Structured output of feature-based sentiment and insights, ready for research or product evaluation.
- **Extensible CrewAI Framework**: Easily add, configure, and coordinate agents for new domains or research tasks.
- **Debug & Logging Utilities**: Built-in debug functions and extensive logging for workflow transparency and troubleshooting.

---

## Agentic Architecture

MajorProj utilizes an agentic paradigm via CrewAI, where each agent fulfills a specialized role:

- **Review Scraper Agent**
  - Scrapes reviews from Amazon using Selenium and BeautifulSoup.
  - Saves structured data (title, text, rating, etc.) to CSV.
- **Feature Extraction Agent**
  - Analyzes review texts to extract salient product features.
  - Supports JSON-based output for downstream analysis.
- **Sentiment Analysis Agent**
  - Assigns sentiment scores to extracted features.
  - Aggregates insights for report generation.
- **Task Orchestration**
  - Defined in `config/tasks.yaml` and `config/agents.yaml` for each flow.
  - Agents collaborate sequentially or in parallel as configured.

**Sample Extracted Features:**
- Comfort, Durability, Fit, Support, Material Quality, Breathability, Traction, Weight, Style, Value for Money
- Display Quality, Battery Life, Storage Capacity, Portability, User Interface, Connectivity, Price

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dimsas04/MajorProj.git
   cd MajorProj
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Python 3.9+ required. See `requirements.txt` for full dependency list (CrewAI, LangChain, Selenium, Pydantic, etc.)*

---

## Running the Project

To launch an agent flow (e.g., `revify_flow`):

```bash
crewai run
```

This command initializes the agent crew, triggering the full pipeline from review scraping to feature-based report generation.

- The system will create a `report.md` summarizing findings in the root directory.
- For custom tasks or agents, modify `config/tasks.yaml` and `config/agents.yaml`.

---

## Configuration

- **Agents & Tasks:**  
  Configure agent roles, skills, and task assignments in:
  - `revify_flow/config/agents.yaml`
  - `revify_flow/config/tasks.yaml`

- **Debugging:**  
  Dedicated debug functions (`debug_scraper_tool`, `debug_run_workflow`) in `revify_flow/src/revify_flow/main.py` allow step-by-step validation and logging.

---

## Technologies Used

- **[CrewAI](https://crewai.com):** Multi-agent orchestration framework
- **Python Ecosystem:**  
  - Data: pandas, numpy
  - AI: langchain, pydantic, langgraph, openai
  - Web Scraping: selenium, beautifulsoup4
- **Logging & Debugging:** Python logging, tracebacks
- **Configuration:** YAML, dotenv
- **Other:** Google Cloud, Matplotlib, OpenCV (for future extensibility)

---

## Support

For questions, feedback, or to contribute:

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Join CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with CrewAI Docs](https://chatg.pt/DWjSBZn)

---

Let's create wonders together with the power and simplicity of agentic AI!

