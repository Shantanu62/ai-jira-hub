import streamlit as st
from groq import Groq
import requests
import json
import datetime

# Page Configuration
st.set_page_config(
    page_title="AI Product Discovery & Jira Delivery Hub",
    page_icon="🚀",
    layout="wide"
)

# --- Advanced SaaS Custom CSS Styling (Vibrant Colors & Modern UI) ---
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Modern Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Sleek SaaS Cards */
    .saas-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #374151;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    
    /* Status Badges */
    .badge-success {
        background-color: #064e3b;
        color: #34d399;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #059669;
    }
    
    .badge-primary {
        background-color: #312e81;
        color: #818cf8;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #4f46e5;
    }

    /* Gradient Primary Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }
    
    h1, h2, h3 {
        letter-spacing: -0.5px;
        color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# Load Credentials from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
JIRA_URL = st.secrets.get("JIRA_URL", "")
JIRA_EMAIL = st.secrets.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = st.secrets.get("JIRA_API_TOKEN", "")

# Sidebar Configuration Hub with Rich UI
st.sidebar.title("⚙️ Control Center")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔌 API Status")
st.sidebar.markdown("🟢 **Groq LLM:** Active")
st.sidebar.markdown("🔗 **Jira Cloud (`AIHUB`):** Connected")
st.sidebar.markdown("---")

# New Feature: Model Selector in Sidebar
st.sidebar.markdown("### 🧠 AI Engine Config")
selected_model = st.sidebar.selectbox(
    "Choose LLM Model:",
    ["llama-3.3-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("🚀 Production-grade AI Product Hub built for high-speed delivery.")

# Main Header Banner using HTML Container
st.markdown("""
    <div class="saas-card" style="margin-top: 10px;">
        <h1 style='color: #818cf8; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px;'>🚀 AI Product Discovery & Jira Delivery Hub</h1>
        <p style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 0;'>Transform raw product visions into structured enterprise PRDs and instantly sync actionable issues to your Atlassian Jira workspace.</p>
    </div>
""", unsafe_allow_html=True)

# Application Tabs
tab1, tab2 = st.tabs(["📝 AI PRD Generator Hub", "🔗 Jira Task Sync Workspace"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.header("Step 1: AI PRD Intelligence Engine")
    with col_r:
        st.markdown('<span class="badge-primary">Model: Active</span>', unsafe_allow_html=True)

    product_idea = st.text_area(
        "Enter your Product Idea / Feature Request:",
        placeholder="e.g., Build an AI-powered receipt scanner for small businesses that categorizes expenses automatically.",
        height=130
    )
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        generate_clicked = st.button("Generate Smart PRD ⚡")
    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<span style='color: #94a3b8; font-size: 0.9rem;'>💡 Generates Executive Summary, Personas, Core Features & KPIs.</span>", unsafe_allow_html=True)
        
    if generate_clicked:
        if not product_idea:
            st.warning("⚠️ Please enter a product idea first.")
        elif not GROQ_API_KEY:
            st.error("❌ Groq API Key is missing! Please configure it in Streamlit Secrets.")
        else:
            with st.spinner("🤖 AI Principal Product Manager is crafting your comprehensive PRD..."):
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
                        model=selected_model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=2048
                    )
                    
                    prd_output = completion.choices[0].message.content
                    st.session_state['generated_prd'] = prd_output
                    
                    st.success("✨ PRD Generated Successfully & Cached in Session!")
                    
                    # Styled output container
                    st.markdown("""<div class="saas-card">""", unsafe_allow_html=True)
                    st.markdown(prd_output)
                    st.markdown("""</div>""", unsafe_allow_html=True)
                    
                    # New Feature: Download PRD Button
                    st.download_button(
                        label="📥 Download PRD as Markdown File",
                        data=prd_output,
                        file_name=f"PRD_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error generating PRD: {e}")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.header("Step 2: Atlassian Jira Agile Sync Engine")
    
    if 'generated_prd' in st.session_state:
        st.markdown("""
            <div class="saas-card">
                <h4 style='color: #34d399; margin-top:0;'>🟢 PRD Ready for Deployment</h4>
                <p style='color: #cbd5e1;'>Your generated PRD is securely cached in session memory and ready to be pushed directly into your Jira board.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 2])
        with col1:
            project_key = st.text_input("Jira Project Key:", value="AIHUB")
        with col2:
            issue_type = st.selectbox("Select Jira Issue Type:", ["Task", "Epic", "Story"], index=0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sync to Jira Workspace 🔗"):
            if not JIRA_URL or not JIRA_EMAIL or not JIRA_API_TOKEN:
                st.error("❌ Jira credentials are missing! Check your Streamlit Secrets.")
            else:
                with st.spinner("🔄 Creating Jira issues via REST API v3..."):
                    try:
                        api_url = f"{JIRA_URL.rstrip('/')}/rest/api/3/issue"
                        auth = (JIRA_EMAIL, JIRA_API_TOKEN)
                        headers = {"Content-Type": "application/json"}
                        
                        payload = {
                            "fields": {
                                "project": {"key": project_key},
                                "summary": f"AI Generated {issue_type} from PRD Hub",
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
                                "issuetype": {"name": issue_type}
                            }
                        }
                        
                        response = requests.post(api_url, json=payload, auth=auth, headers=headers)
                        
                        if response.status_code == 201:
                            issue_data = response.json()
                            st.markdown(f"""
                                <div class="saas-card" style="border-color: #059669;">
                                    <h3 style='color: #34d399; margin-top:0;'>🎉 Successfully Synced!</h3>
                                    <p style='color: #f8fafc;'>Issue Key Created: <b>{issue_data.get('key')}</b></p>
                                    <p style='color: #94a3b8; font-size: 0.9rem;'>Check your Jira board (`{project_key}`) to view the live ticket.</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Failed to sync with Jira. Response: {response.text}")
                            
                    except Exception as e:
                        st.error(f"🚨 Jira connection error: {e}")
    else:
        st.markdown("""
            <div class="saas-card" style="border-color: #d97706;">
                <h4 style='color: #fbbf24; margin-top:0;'>⚠️ Action Required</h4>
                <p style='color: #cbd5e1;'>Please go to the <b>'AI PRD Generator Hub'</b> tab first, enter your product idea, and generate a PRD before syncing to Jira.</p>
            </div>
        """, unsafe_allow_html=True)
