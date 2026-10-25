# 🚀 AI Product Discovery & Jira Delivery Hub

An end-to-end, standalone web application designed to bridge the gap between high-level product ideation and agile execution. Built for modern Product Managers to instantly generate comprehensive Product Requirements Documents (PRDs) using advanced LLMs and automatically sync actionable tasks to Atlassian Jira.

---

## ✨ Key Features

* **📝 AI PRD Generator:** Powered by high-speed Groq LLMs to instantly transform raw, unstructured product ideas into structured PRDs (Executive Summary, Target Personas, Core Features, Non-Functional Requirements, and Success Metrics/KPIs).
* **🔗 Automated Jira Task Sync:** Seamlessly parses generated product requirements and pushes actionable tasks directly to an Atlassian Jira workspace using the Jira REST API v3.
* **🌐 Standalone Cloud Architecture:** Designed as a fully integrated Streamlit application, eliminating external backend dependencies for smooth 24/7 deployment on Streamlit Cloud.

---

## 🛠️ Tech Stack & Architecture

* **Frontend & Framework:** Python, Streamlit (Hosted live on Streamlit Cloud)
* **AI / LLM Engine:** Groq API 
* **Project Management Integration:** Atlassian Jira REST API v3
* **Version Control:** Git & GitHub

---

## ⚙️ Configuration & Secrets Management

To run this application, configure the following secrets in your Streamlit Cloud dashboard (`Settings -> Secrets`):

```toml
GROQ_API_KEY = "your_groq_api_key_here"
JIRA_URL = "[https://your-domain.atlassian.net](https://your-domain.atlassian.net)"
JIRA_EMAIL = "your-email@domain.com"
JIRA_API_TOKEN = "your_jira_api_token_here"