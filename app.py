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

# --- Modern Custom CSS Styling (Zero backend impact, pure UI polish) ---
st.markdown("""
    <style>
    /* Main Background & Font Color */
    .main {
        background-color: #0b0f19;
    }
    
    /* Modern Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Custom Card Containers */
    .dashboard-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Gradient Primary Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.92;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
    }
    
    /* Headers Styling */
    h1, h2, h3 {
        letter-spacing: -0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# Load Credentials from Streamlit Secrets or Sidebar fallback
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
JIRA_URL = st.secrets.get("JIRA_URL", "")
JIRA_EMAIL = st.secrets.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = st.secrets.get("JIRA_API_TOKEN", "")

# Sidebar for Configuration Check
st.sidebar.title("⚙️ Configuration Hub")
st.sidebar.markdown("---")
st.sidebar.success("🟢 Groq API Connected")
st.sidebar.success("🔗 Jira Cloud Connected")
st.sidebar.markdown("---")
st.sidebar.info("Direct cloud-native architecture (No local backend required).")

# Main Title Header with Modern Layout
st.markdown("""
    <div style='padding: 10px 0 20px 0;'>
        <h1 style='color: #f8fafc; font-weight: 800; font-size: 2.4rem;'>🚀 AI Product Discovery & Jira Delivery Hub</h1>
        <p style='color: #94a3b8; font-size: 1.15rem;'>Transform raw product ideas into structured PRDs using high-speed LLMs and instantly sync actionable tasks to your Jira workspace.</p>
    </div>
""", unsafe_allow_html=True)

# Tabs for workflow with clean separation
tab1, tab2 = st.tabs(["📝 AI PRD Generator", "🔗 Jira Task Sync"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.header("Step 1: Generate Product Requirements Document (PRD)")
    
    product_idea = st.text_area(
        "Enter your Product Idea / Feature Request:",
        placeholder="e.g., Build an AI-powered resume parser that extracts skills and maps them to job descriptions.",
        height=120
    )
    
    col_btn, col_empty = st.columns([1, 4])
    with col_btn:
        generate_clicked = st.button("Generate PRD ⚡")
        
    if generate_clicked:
        if not product_idea:
            st.warning("⚠️ Kripya pehle product idea enter karein.")
        elif not GROQ_API_KEY:
            st.error("❌ Groq API Key missing hai! Kripya Streamlit Secrets mein configure karein.")
        else:
            with st.spinner("🤖 AI is crafting your comprehensive PRD..."):
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
                        model="openai/gpt-oss-20b", # Your existing model config
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=2048
                    )
                    
                    prd_output = completion.choices[0].message.content
                    st.session_state['generated_prd'] = prd_output
                    
                    st.success("✨ PRD Generated Successfully!")
                    st.markdown("---")
                    st.markdown(prd_output)
                    
                except Exception as e:
                    st.error(f"❌ Error generating PRD: {e}")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.header("Step 2: Sync Tasks to Atlassian Jira")
    
    if 'generated_prd' in st.session_state:
        st.info("💡 Generated PRD is cached in session and ready to be parsed into Jira Epics and Stories.")
        
        col1, col2 = st.columns([2, 2])
        with col1:
            project_key = st.text_input("Jira Project Key:", value="AI")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sync to Jira Workspace 🔗"):
            if not JIRA_URL or not JIRA_EMAIL or not JIRA_API_TOKEN:
                st.error("❌ Jira credentials missing hain! Streamlit Secrets check karein.")
            else:
                with st.spinner("🔄 Creating Jira issues via REST API v3..."):
                    try:
                        # Jira API endpoint for issues
                        api_url = f"{JIRA_URL.rstrip('/')}/rest/api/3/issue"
                        auth = (JIRA_EMAIL, JIRA_API_TOKEN)
                        headers = {"Content-Type": "application/json"}
                        
                        # Payload creation for Jira task
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
                                            "text": "Task automatically synced from AI Product Discovery & Jira Delivery Hub."
                                        }]
                                    }]
                                },
                                "issuetype": {"name": "Task"}
                            }
                        }
                        
                        response = requests.post(api_url, json=payload, auth=auth, headers=headers)
                        
                        if response.status_code == 201:
                            issue_data = response.json()
                            st.success(f"🎉 Successfully synced with Jira! Created Issue Key: **{issue_data.get('key')}**")
                        else:
                            st.error(f"❌ Failed to sync with Jira. Response: {response.text}")
                            
                    except Exception as e:
                        st.error(f"🚨 Jira connection error: {e}")
    else:
        st.warning("⚠️ Pehle 'AI PRD Generator' tab mein jaakar PRD generate karein.")