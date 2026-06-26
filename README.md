````markdown
# 💊 PharmaWatch AI
### Multi-Agent AI Platform for Predicting Drug Shortages & Strengthening Healthcare Supply Chains



**Predict. Analyze. Prepare.**

*Turning global healthcare intelligence into proactive decisions.*

</p>

---

# 📖 Overview

Medicine shortages continue to disrupt healthcare systems across the world. Hospitals often become aware of shortages only after inventories reach critically low levels, leaving little time to respond.

**PharmaWatch AI** is an AI-powered healthcare supply chain intelligence platform designed to predict potential medicine shortages before they become critical.

Unlike traditional monitoring systems that rely only on historical inventory data, PharmaWatch AI continuously gathers information from global events, pharmaceutical research, and healthcare intelligence using multiple AI agents. The platform analyzes these signals to estimate supply risks, identify vulnerable medicines, simulate disruption scenarios, and recommend therapeutic alternatives.

By combining Large Language Models (LLMs), Multi-Agent AI, structured data validation, and interactive visualizations, PharmaWatch AI enables healthcare organizations to move from reactive crisis management to proactive decision-making.

---

# 🚨 Problem Statement

Healthcare supply chains are becoming increasingly vulnerable due to:

- Natural disasters
- Geopolitical conflicts
- Manufacturing delays
- API (Active Pharmaceutical Ingredient) shortages
- Transportation disruptions
- Disease outbreaks
- Regulatory restrictions
- Sudden demand surges

Most hospitals and healthcare providers identify shortages only after inventories become critically low.

The absence of an intelligent early-warning system results in:

- Delayed patient treatments
- Increased operational costs
- Emergency procurement
- Resource mismanagement
- Reduced healthcare resilience

---

# 💡 Our Solution

PharmaWatch AI introduces an AI-driven decision support system capable of continuously monitoring healthcare intelligence and predicting medicine shortages before they impact patient care.

The platform combines multiple specialized AI agents that collaborate to:

- Monitor global healthcare events
- Analyze pharmaceutical research
- Evaluate supply chain risks
- Predict medicine shortages
- Simulate disruption scenarios
- Recommend alternative medicines
- Present insights through interactive dashboards

Instead of simply reporting shortages, PharmaWatch AI explains *why* they may occur and helps decision-makers prepare accordingly.

---

# ✨ Key Features

## 📊 Intelligent Dashboard

A centralized dashboard providing real-time healthcare supply chain insights.

Features include:

- Medicine risk overview
- High-risk medicines
- Risk distribution
- Interactive charts
- Supply chain analytics
- Decision support metrics

---

## 🤖 AI-Based Drug Shortage Prediction

Predicts the likelihood of future medicine shortages using AI-driven reasoning and structured analysis.

Outputs include:

- Risk Score
- Shortage Probability
- Risk Category
- Decision Recommendations

---

## 🌍 Global Event Intelligence

The platform continuously analyzes global events that may impact pharmaceutical supply chains.

Examples include:

- Natural disasters
- Political instability
- Manufacturing shutdowns
- Transportation disruptions
- International logistics issues

---

## 📚 Pharmaceutical Research Intelligence

Research Agent collects and summarizes relevant healthcare and pharmaceutical information to identify emerging risks before they affect medicine availability.

---

## 🏥 Hospital Supply Chain Simulation

Simulates how supply disruptions affect hospital operations.

Users can model scenarios using:

- Hospital bed capacity
- Medicine demand
- Duration of disruption
- Disaster type

The simulation estimates operational impact and helps hospitals prepare contingency plans.

---

## 💊 Drug Alternatives

Suggests therapeutic alternatives whenever a medicine faces potential shortages.

> **Disclaimer:** Recommendations are intended solely for supply-chain planning and must always be reviewed by licensed healthcare professionals.

---

## 📈 Interactive Data Visualization

Visual dashboards built using Plotly provide insights into:

- Risk trends
- Medicine comparisons
- Supply chain performance
- Shortage probabilities
- Healthcare intelligence

---

# 🧠 Multi-Agent AI Architecture

Unlike traditional machine learning applications, PharmaWatch AI follows a **Multi-Agent AI Architecture**.

Each AI agent performs a specialized responsibility before collaborating to generate the final prediction.

---

## 🔍 Event Agent

Responsible for monitoring global events that may disrupt pharmaceutical supply chains.

Examples:

- Natural disasters
- Geopolitical conflicts
- Transportation failures
- Manufacturing disruptions

---

## 📚 Research Agent

Analyzes pharmaceutical research and healthcare intelligence.

Responsibilities include:

- Summarizing medical research
- Identifying emerging healthcare risks
- Supporting evidence-based predictions

---

## ⚠️ Risk Agent

Combines outputs from other agents to estimate medicine shortage risks.

Produces:

- Risk Scores
- Shortage Assessments
- Decision Recommendations

---

# 🏗️ System Architecture

```text
                    👤 User
                       │
                       ▼
             Streamlit Web Application
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Drug Prediction  Hospital Simulation  Drug Alternatives
                       │
                       ▼
             AI Agent Orchestrator
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Event Agent     Research Agent     Risk Agent
      │                │                │
      ▼                ▼                ▼
 Event Chain     Research Chain     Risk Chain
      │                │                │
      └──────────────┬─────────────────┘
                     ▼
           Prompt Engineering Layer
                     ▼
              Large Language Model
                     ▼
        Structured Schema Validation
                     ▼
 External Intelligence Sources
     • GDELT Global Events
     • News Intelligence
     • Research Intelligence
                     ▼
          AI Decision Support Engine
                     ▼
         Interactive Streamlit Dashboard
```

---

# ⚙️ Project Workflow

```text
User Input
      │
      ▼
Input Validation
      │
      ▼
AI Agent Execution
      │
      ├──────────────┐
      ▼              ▼
 Event Agent   Research Agent
      │              │
      └──────┬───────┘
             ▼
        Risk Agent
             │
             ▼
External Intelligence Services
             │
             ▼
Structured Validation
             │
             ▼
Decision Generation
             │
             ▼
Interactive Dashboard
```

---

# 📂 Project Structure

```text
PharmaWatch-AI/
│
├── agents/
│   ├── event_agent.py
│   ├── research_agent.py
│   └── risk_agent.py
│
├── chains/
│   ├── event_chain.py
│   ├── research_chain.py
│   └── risk_chain.py
│
├── llm/
│   └── llm.py
│
├── models/
│   ├── event_schema.py
│   ├── raw_article.py
│   ├── research_schema.py
│   └── risk_schema.py
│
├── prompts/
│   ├── event_prompt.py
│   ├── research_prompt.py
│   └── risk_prompt.py
│
├── services/
│   ├── gdelt_service.py
│   ├── news_service.py
│   └── research_service.py
│
├── utils/
│
├── app.py
├── main.py
├── config.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|-----------|--------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Framework | LangChain |
| LLM Integration | OpenAI Compatible LLM |
| AI Architecture | Multi-Agent AI |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| News Intelligence | GDELT |
| Research Intelligence | Research APIs |
| Validation | Pydantic Models |
| Development | VS Code |
| Version Control | Git & GitHub |

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Ram310105/PharmaWatch-AI.git
cd PharmaWatch-AI
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create a `.env` file and add your required API keys.

```env
OPENAI_API_KEY=your_key
NEWS_API_KEY=your_key
```

## Run the Application

```bash
streamlit run app.py
```

---

# 🌍 Real-World Applications

PharmaWatch AI can assist:

- 🏥 Hospitals
- 💊 Pharmaceutical Manufacturers
- 🚚 Medical Distributors
- 🏛 Government Health Departments
- 🌐 NGOs
- 📦 Healthcare Supply Chain Managers

---

# 🔮 Future Enhancements

- Real-time pharmaceutical inventory integration
- Time-series forecasting models
- Multi-country healthcare intelligence
- Explainable AI (XAI)
- Autonomous procurement recommendations
- Live supply chain monitoring
- Email and SMS alerts
- Regional shortage forecasting
- Cloud-native deployment
- Role-based dashboards

---

# 👨‍💻 Developed By

**Code Force Team**

Passionate about building intelligent AI systems that solve real-world healthcare challenges through Machine Learning, Large Language Models, and Multi-Agent AI.

---

# ⭐ Support

If you found this project useful or interesting, please consider giving it a ⭐ on GitHub.

Your support encourages further development and innovation.
````
