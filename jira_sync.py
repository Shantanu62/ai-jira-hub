import os
import json
import builtins
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Force print statements to flush immediately in Uvicorn terminal
_original_print = builtins.print
def print(*args, **kwargs):
    kwargs.setdefault('flush', True)
    _original_print(*args, **kwargs)

load_dotenv()

# Environment variables support both naming conventions to prevent missing config
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL") or os.getenv("JIRA_URL")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL") or os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN) if JIRA_USER_EMAIL and JIRA_API_TOKEN else None
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def create_jira_issues(prd_data: dict) -> dict:
    print("\n==========================================")
    print("🚀 === JIRA SYNC PROCESS STARTED ===")
    print("==========================================")
    print(f"📌 Jira Base URL: {JIRA_BASE_URL}")
    print(f"📌 Jira Project Key: {JIRA_PROJECT_KEY}")
    
    # Debugging: Print incoming PRD data structure
    print("\n📦 Received PRD Data for Jira Sync:")
    print(json.dumps(prd_data, indent=2))

    if not JIRA_BASE_URL or not JIRA_USER_EMAIL or not JIRA_API_TOKEN or not JIRA_PROJECT_KEY:
        print("⚠️ ERROR: Jira environment variables are missing or incomplete in .env!")
        return {"status": "error", "message": "Jira credentials missing in .env"}

    created_issues = []
    url = f"{JIRA_BASE_URL.rstrip('/')}/rest/api/3/issue"

    # Handle potential key variations from AI response
    epics = prd_data.get("epics") or prd_data.get("features") or prd_data.get("modules") or []

    if not epics:
        print("⚠️ Warning: No epics/features found in the PRD data!")
        return {"status": "warning", "message": "No epics found in PRD data to sync.", "created_issues": []}

    for epic in epics:
        epic_name = epic.get("epic_name") or epic.get("title") or epic.get("name") or "Untitled Epic"
        epic_desc = epic.get("description") or epic.get("summary") or "No description provided."

        # 1. Create Epic
        epic_payload = {
            "fields": {
                "project": {"key": JIRA_PROJECT_KEY},
                "summary": epic_name,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{"type": "paragraph", "content": [{"type": "text", "text": epic_desc}]}]
                },
                "issuetype": {"name": "Epic"}
            }
        }

        print(f"\n⏳ Creating Epic: '{epic_name}'...")
        response = requests.post(url, json=epic_payload, headers=headers, auth=auth)
        
        if response.status_code != 201:
            print(f"❌ Failed to create Epic '{epic_name}': {response.status_code} - {response.text}")
            continue
            
        epic_data = response.json()
        epic_key = epic_data.get("key")
        print(f"✅ Successfully Created Epic -> KEY: {epic_key}")
        created_issues.append({"epic": epic_key, "summary": epic_name})

        # 2. Create User Stories under Epic
        stories = epic.get("user_stories") or epic.get("stories") or epic.get("tasks") or []
        for story in stories:
            story_title = story.get("title") or story.get("summary") or "Untitled Story"
            story_desc = story.get("description") or "No description provided."

            story_payload = {
                "fields": {
                    "project": {"key": JIRA_PROJECT_KEY},
                    "summary": story_title,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [{"type": "paragraph", "content": [{"type": "text", "text": story_desc}]}]
                    },
                    "issuetype": {"name": "Task"} 
                }
            }

            print(f"  ⏳ Creating Task under {epic_key}: '{story_title}'...")
            story_response = requests.post(url, json=story_payload, headers=headers, auth=auth)
            
            if story_response.status_code == 201:
                story_key = story_response.json().get("key")
                print(f"  ✅ Successfully Created Task -> KEY: {story_key}")
                created_issues.append({"story": story_key, "summary": story_title})
            else:
                print(f"  ❌ Failed to create Task '{story_title}': {story_response.status_code} - {story_response.text}")

    print("\n==========================================")
    print(f"🎉 === JIRA SYNC COMPLETED. Total issues created: {len(created_issues)} ===")
    print("==========================================\n")
    return {"status": "success", "created_issues": created_issues}