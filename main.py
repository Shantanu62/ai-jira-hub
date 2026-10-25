from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

from ai_extractor import generate_prd_and_jira_tasks
from jira_sync import create_jira_issues

app = FastAPI(title="AI Product Discovery & Jira Delivery Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductIdeaRequest(BaseModel):
    idea: str

@app.get("/")
def read_root():
    return {"message": "AI Product Discovery API is up and running!"}

@app.post("/api/generate-and-sync")
def generate_and_sync(request: ProductIdeaRequest):
    if not request.idea.strip():
        raise HTTPException(status_code=400, detail="Product idea cannot be empty.")
    
    try:
        prd_data = generate_prd_and_jira_tasks(request.idea)
        jira_response = create_jira_issues(prd_data)
        
        return {
            "status": "success",
            "prd": prd_data,
            "jira": jira_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))