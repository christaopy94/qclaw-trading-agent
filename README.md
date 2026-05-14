<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Architecture-Multi--Agent-ff6b6b?logo=robotframework&logoColor=white" alt="Multi-Agent" />
<img src="https://img.shields.io/badge/Workflow-AI_Automation-10b981?logo=openai&logoColor=white" alt="AI Workflow" />
<img src="https://img.shields.io/badge/Domain-Financial_Analysis-6366f1?logo=bloomberg&logoColor=white" alt="Financial Analysis" />
<img src="https://img.shields.io/badge/Reasoning-Long_Chain-8b5cf6?logo=chainlink&logoColor=white" alt="Long Chain Reasoning" />
<img src="https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white" alt="MIT License" />

</div>

<h1 align="center">🤖 QClaw FinAgent</h1>
<h3 align="center"><em>Multi-Agent Financial Market Analysis & Review Automation System</em></h3>

<p align="center">
  <strong>A production-grade AI Agent orchestration system for Chinese A-share market analysis, combining multi-agent collaboration with long-chain reasoning to deliver structured daily market reviews — with zero trading execution.</strong>
</p>

---

## 📖 Overview

**QClaw FinAgent** is an AI-native multi-agent workflow system designed for the Chinese financial market (A-shares). It orchestrates a team of specialized LLM agents — data collection, sentiment analysis, strategy reasoning, review generation, and notification delivery — to produce daily market intelligence reports automatically.

> ⚠️ **This is NOT a trading bot.** QClaw FinAgent performs **market information analysis only**. It does not place orders, manage portfolios, or generate buy/sell signals. It is a **decision-support workflow** for research and educational purposes.

### 🎯 Why This Project Exists

- **Demonstrate Multi-Agent Orchestration** — 5+ agents collaborating through a structured workflow pipeline
- **Showcase Long-Chain Reasoning** — Agents analyze multi-dimensional data (price action, sentiment, themes, fund flows) before generating structured output
- **Prove Chinese Market AI Capability** — Specialized prompts and analysis patterns for the unique dynamics of A-share markets
- **Platform-Ready Architecture** — Clean separation of concerns, ready for integration with AI platforms (e.g., Xiaomi MiMo)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        QClaw FinAgent                           │
│                     (Multi-Agent Orchestrator)                   │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐      ┌───────────────┐
│ Data Agent    │     │Sentiment Agent│      │ Strategy Agent│
│               │     │               │      │               │
│ • Market data │     │ • News emotion│      │ • Theme rot.  │
│ • Limit boards│     │ • Social buzz │      │ • Fund flow   │
│ • Price action│     │ • Market fear │      │ • Sector heat │
│ • Volume flow │     │ • Consensus   │      │ • Leader ID   │
└───────┬───────┘     └───────┬───────┘      └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                    ┌───────────────────┐
                    │   Review Agent    │
                    │                   │
                    │ • Structured gen  │
                    │ • Multi-pass refine│
                    │ • Risk assessment │
                    │ • Forward outlook │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Notify Agent     │
                    │                   │
                    │ • DingTalk/WeChat │
                    │ • Markdown format │
                    │ • Scheduled push  │
                    └───────────────────┘
```

### Agent Responsibilities

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Data Agent** | Raw market data collection | Market APIs, data sources | Structured market snapshot |
| **Sentiment Agent** | Multi-source sentiment analysis | News, social media, forums | Sentiment score + trend |
| **Strategy Agent** | Theme rotation & leader identification | Data + Sentiment outputs | Theme map + candidate list |
| **Review Agent** | Structured review generation | All upstream outputs | Final markdown review |
| **Notify Agent** | Multi-channel delivery | Review output | Webhook push |

---

## 🔄 Multi-Agent Workflow

```
[Daily Trigger 15:30 CST]
          │
          ▼
┌─────────────────┐
│  1. Data Agent   │──── Collects: boards, prices, volumes, fund flows
└────────┬────────┘
         │ structured_data.json
         ▼
┌─────────────────┐
│ 2. Sentiment Agt │──── Analyzes: news tone, social buzz, fear/greed
└────────┬────────┘
         │ sentiment_report.json
         ▼
┌─────────────────┐
│ 3. Strategy Agt  │──── Reasons: sector rotation, leading stocks, themes
└────────┬────────┘
         │ strategy_analysis.json
         ▼
┌─────────────────┐
│ 4. Review Agent  │──── Generates: structured daily review (multi-pass)
└────────┬────────┘
         │ daily_review.md
         ▼
┌─────────────────┐
│ 5. Notify Agent  │──── Delivers: webhook push to DingTalk / WeChat / Slack
└─────────────────┘
```

### Long-Chain Reasoning

Each agent performs **multi-step reasoning** before producing output:

- **Data Agent**: raw query → filter → categorize → structure
- **Sentiment Agent**: fetch → extract → score → aggregate → trend
- **Strategy Agent**: map themes → identify leaders → cross-validate → rank
- **Review Agent**: synthesize → draft → refine → format → validate

This chain produces **depth of analysis** unachievable with single-pass LLM calls.

---

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🔄 **Multi-Agent Pipeline** | 5 specialized agents with structured handoff | ✅ |
| 🧠 **Long-Chain Reasoning** | Multi-step analysis per agent, not single-pass | ✅ |
| 📊 **Market Data Aggregation** | Limit boards, sector rotation, fund flows | ✅ |
| 💬 **Sentiment Analysis** | News + social media emotion scoring | ✅ |
| 🎯 **Theme Identification** | Sector rotation & leading stock mapping | ✅ |
| 📝 **Automated Review Generation** | Structured markdown daily reports | ✅ |
| 📨 **Multi-Channel Notification** | DingTalk, WeChat, Slack webhook push | ✅ |
| ⚙️ **YAML Configuration** | All parameters configurable, zero hardcode | ✅ |
| 📅 **Scheduled Execution** | Auto-triggered at market close (15:30 CST) | ✅ |
| 🔌 **Platform-Ready** | Interface ready for MiMo / AI platform integration | 🚧 |

---

## 🛠️ Tech Stack

```yaml
Core:
  - Python 3.10+
  - asyncio (async agent orchestration)

LLM Integration:
  - OpenAI-compatible API (GPT-4 / DeepSeek / Qwen / Claude)
  - LangChain (optional, for tool-use patterns)

Data Sources:
  - AkShare (A-share market data)
  - Public financial news APIs
  - Social sentiment scraping (optional)

Output & Delivery:
  - Markdown report generation
  - Webhook clients (DingTalk, WeChat Work, Slack)
  - File-based output storage

Infrastructure:
  - YAML configuration
  - Structured logging (loguru)
  - Pydantic data validation
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- LLM API key (OpenAI-compatible)
- A-share data access (AkShare or equivalent)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/qclaw-fin-agent.git
cd qclaw-fin-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
cp config/.env.example config/.env
# Edit config/.env with your API keys and settings
```

### Run

```bash
# Single run (manual trigger)
python main.py --run-once

# Scheduled mode (auto-trigger at 15:30 CST daily)
python main.py --schedule

# Run with specific date (backfill)
python main.py --run-once --date 2026-05-14
```

---

## 📋 Example Output

A complete daily review generated by the system:

```markdown
# 📊 A-Share Market Daily Review — 2026-05-14

## 🎭 Sentiment Positioning: 分歧修复 (Divergence Repair)

## 📈 Market Snapshot
- **Limit-Up Count**: 47 | **Limit-Down**: 8
- **Highest Board**: 5连板 (5 consecutive limit-ups)
- **Turnover**: ¥892B (↑12% vs yesterday)

## 🔥 Theme Heatmap
| Sector | Strength | Leaders |
|--------|----------|---------|
| AI Applications | 🔥🔥🔥 | xx科技, xx智能 |
| New Energy | 🔥🔥 | xx股份, xx材料 |
| Consumer | 🔥 | xx集团 |

## 🎯 Key Observations
1. AI application sector shows sustained momentum
2. New energy saw profit-taking in afternoon session
3. Low-float small-caps outperformed large-caps

## ⚠️ Risk Notes
- High-board stocks showing divergence signals
- Afternoon turnover spike suggests short-term profit pressure

---
*Generated by QClaw FinAgent — Multi-Agent Review System*
*For market analysis purposes only. Not financial advice.*
```

---

## 🗺️ Roadmap

- [x] Multi-Agent Review Pipeline
- [x] Webhook Notification (DingTalk / WeChat / Slack)
- [x] Structured Markdown Output
- [x] YAML Configuration System
- [x] Async Agent Orchestration
- [ ] Real-time Data Streaming (WebSocket)
- [ ] Level-2 Market Data Integration
- [ ] MiMo Platform Native Optimization
- [ ] Multi-Market Expansion (HK, US)
- [ ] Interactive Dashboard (Web UI)
- [ ] Agent Memory & Learning from Historical Reviews
- [ ] Voice Output via TTS Integration

---

## 📁 Project Structure

```
qclaw-fin-agent/
├── agents/                    # Specialized AI agents
│   ├── __init__.py
│   ├── data_agent.py          # Market data collection
│   ├── sentiment_agent.py     # Sentiment & emotion analysis
│   ├── strategy_agent.py      # Theme rotation & leader ID
│   ├── review_agent.py        # Structured review generation
│   └── notify_agent.py        # Webhook notification delivery
├── workflows/                 # Agent orchestration pipelines
│   ├── __init__.py
│   └── daily_review_workflow.py
├── prompts/                   # LLM prompt templates
│   └── system_prompt.md
├── config/                    # Configuration files
│   ├── settings.yaml
│   └── .env.example
├── output/                    # Generated review output
├── screenshots/               # Demo screenshots
├── docs/                      # Documentation
│   └── demo.md
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## ⚠️ Disclaimer

**QClaw FinAgent is a market analysis and AI workflow research tool. It is NOT a trading system.**

- ❌ **Not Financial Advice**: All generated content is for informational purposes only. Nothing constitutes investment advice, recommendations, or solicitation.
- ❌ **No Trade Execution**: This system does NOT execute trades, manage portfolios, or interact with brokerage APIs.
- ❌ **No Performance Guarantees**: Past market patterns do not predict future results. AI-generated analysis may contain errors or biases.
- ✅ **Research Only**: This project demonstrates multi-agent AI orchestration, long-chain reasoning, and automated information processing for the Chinese financial market.
- ✅ **Educational Purpose**: Suitable for AI developers, researchers, and students studying multi-agent systems and financial NLP.

**Use this software at your own risk. The authors assume no liability for any financial decisions made based on outputs from this system.**

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

<div align="center">

**[Documentation](docs/demo.md)** • **[Configuration Guide](config/)** • **[Contributing](CONTRIBUTING.md)**

<sub>Built with ❤️ for AI Workflow Research | Multi-Agent · Long-Chain Reasoning · Chinese Market AI</sub>

</div>