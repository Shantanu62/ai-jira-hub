import streamlit as st
from groq import Groq
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="AI Product Discovery & Jira Delivery Hub",
    page_icon="🚀",
    layout="wide"
)

# Load Credentials from Streamlit Secrets or Sidebar fallback
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
JIRA_URL = st.secrets.get("JIRA_URL", "")
JIRA_EMAIL = st.secrets.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = st.secrets.get("JIRA_API_TOKEN", "")

# Sidebar for Configuration Check
st.sidebar.title("⚙️ Configuration Hub")
st.sidebar.info("Connected directly to Groq & Jira Cloud APIs (No local backend required).")

# Main Title
st.title("🚀 AI Product Discovery & Jira Delivery Hub")
st.markdown("Transform your raw product ideas into structured PRDs and automatically sync actionable tasks to your Jira workspace.")

# Tabs for workflow
tab1, tab2 = st.tabs(["📝 AI PRD Generator", "🔗 Jira Task Sync"])

with tab1:
    st.header("Step 1: Generate Product Requirements Document (PRD)")
    
    product_idea = st.text_area(
        "Enter your Product Idea / Feature Request:",
        placeholder="e.g., Build an AI-powered resume parser that extracts skills and maps them to job descriptions."
    )
    
    if st.button("Generate PRD"):
        if not product_idea:
            st.warning("Kripya pehle product idea enter karein.")
        elif not GROQ_API_KEY:
            st.error("Groq API Key missing hai! Kripya Streamlit Secrets mein configure karein.")
        else:
            with st.spinner("AI is crafting your PRD..."):
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                    prompt = f"""
                    You are an expert Principal Product Manager. Generate a comprehensive Product Requirements Document (PRD) for the following idea:
                    '{product_idea}'
                    
                    Include:
                    1. Executive Summary & Problem Statement
                    2. Target User Personas
                    3. Core Features & Functional Requirements
                    4. Non-Functional Requirements
                    5. Success Metrics (KPIs)
                    """
                    
                    completion = client.chat.completions.create(
                        model="qwen-2.5-32b", # Ya aap jo model use kar rahe hain
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=2048
                    )
                    
                    prd_output = completion.choices[0].message.content
                    st.session_state['generated_prd'] = prd_output
                    
                    st.success("PRD Generated Successfully!")
                    st.markdown(prd_output)
                    
                except Exception as e:
                    st.error(f"Error generating PRD: {e}")

with tab2:
    st.header("Step 2: Sync Tasks to Atlassian Jira")
    
    if 'generated_prd' in st.session_state:
        st.info("Generated PRD is ready to be parsed into Jira Epics and Stories.")
        
        project_key = st.text_input("Jira Project Key:", value="AI")
        
        if st.button("Sync to Jira"):
            if not JIRA_URL or not JIRA_EMAIL or not JIRA_API_TOKEN:
                st.error("Jira credentials missing hain! Streamlit Secrets check karein.")
            else:
                with st.spinner("Creating Jira issues via REST API..."):
                    try:
                        # Jira API endpoint for issues
                        api_url = f"{JIRA_URL.rstrip('/')}/rest/api/3/issue"
                        auth = (JIRA_EMAIL, JIRA_API_TOKEN)
                        headers = {"Content-Type": "application/json"}
                        
                        # Sample payload creation for Jira task
                        payload = {
                            "fields": {
                                "project": {"key": project_key},
                                "summary": "AI Generated Task from PRD Hub",
                                "description": {
                                    "type": "doc",
                                    "version": 1,
                                    "content": [{
                                        "type": "paragraph",
                                        "content": [{
                                            "type": "text", 
                                            "text": "Task automatically synced from AI Product Discovery Hub."
                                        }]
                                    }]
                                },
                                "issuetype": {"name": "Task"}
                            }
                        }
                        
                        response = requests.post(api_url, json=payload, auth=auth, headers=headers)
                        
                        if response.status_code == 201:
                            issue_data = response.json()
                            st.success(f"Successfully synced with Jira! Issue Key: {issue_data.get('key')}")
                        else:
                            st.error(f"Failed to sync with Jira. Response: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Jira connection error: {e}")
    else:
        st.warning("Pehle 'AI PRD Generator' tab mein jaakar PRD generate karein.")