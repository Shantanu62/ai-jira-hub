import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Product Discovery & Jira Delivery Hub",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Product Discovery & Jira Delivery Hub")
st.markdown("Transform your raw product ideas into structured PRDs and sync them directly to Jira (`AIHUB`) using Gemini AI!")

product_idea = st.text_area(
    "Enter your Product Idea:", 
    placeholder="e.g., Build an AI-powered receipt scanner for small businesses...",
    height=120
)

if st.button("Generate PRD & Sync to Jira", type="primary"):
    if not product_idea.strip():
        st.warning("Please enter a valid product idea first.")
    else:
        with st.spinner("🤖 Generating PRD with AI and syncing tickets to Jira... Please wait."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/generate-and-sync",
                    json={"idea": product_idea},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Successfully generated PRD and synced with Jira!")
                    
                    prd_data = result.get("prd", {})
                    jira_result = result.get("jira", {})
                    
                    prd_text = json.dumps(result, indent=2)
                    st.download_button(
                        label="📥 Download PRD as JSON / Text",
                        data=prd_text,
                        file_name="generated_prd.json",
                        mime="application/json"
                    )
                    
                    st.divider()
                    st.subheader("📄 Generated Product Requirements Document (PRD)")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Product Name:** {prd_data.get('product_name', 'N/A')}")
                        st.markdown(f"**Objective:** {prd_data.get('objective', 'N/A')}")
                    with col2:
                        st.markdown(f"**Target Audience:** {prd_data.get('target_audience', 'N/A')}")
                    
                    st.divider()
                    st.subheader("🎯 Jira Epics & User Stories Synced")
                    
                    epics = prd_data.get("epics", [])
                    jira_domain = "https://laancy321-1792742540398.atlassian.net"
                    
                    for epic in epics:
                        with st.expander(f"📦 Epic: {epic.get('epic_name', 'Epic')}"):
                            st.write(f"**Description:** {epic.get('description', '')}")
                            st.markdown("#### User Stories:")
                            for story in epic.get('user_stories', []):
                                st.markdown(f"- **{story.get('title')}**: {story.get('description')}")
                                criteria = story.get('acceptance_criteria', [])
                                if criteria:
                                    st.markdown("  * *Acceptance Criteria:*")
                                    for ac in criteria:
                                        st.markdown(f"    * {ac}")
                    
                    st.markdown("---")
                    st.markdown(f"🔗 **[Click here to view your Jira Board & Backlog]({jira_domain}/jira/software/projects/AIHUB/boards/3)**")
                    
                else:
                    err_msg = response.json().get("detail", response.text)
                    st.error(f"Backend Error: {err_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to FastAPI backend. Ensure your Uvicorn server is running on port 8000!")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")