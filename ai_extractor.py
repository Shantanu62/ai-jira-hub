import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

# Groq client initialize karein
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_prd_and_jira_tasks(product_idea: str) -> dict:
    prompt = f"""
    You are an expert AI Product Manager and Agile Coach. 
    Analyze the following product idea and generate a comprehensive Product Requirements Document (PRD) along with Jira Epics and User Stories.
    
    Product Idea: {product_idea}
    
    You must return a valid JSON object with the following exact structure:
    {{
      "product_name": "String",
      "objective": "String",
      "target_audience": "String",
      "epics": [
        {{
          "epic_name": "String",
          "description": "String",
          "user_stories": [
            {{
              "title": "String",
              "description": "String",
              "acceptance_criteria": ["String 1", "String 2"]
            }}
          ]
        }}
      ]
    }}
    """

    try:
        # Groq API Call with Llama model and JSON mode enabled
        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",  # Sabse powerful aur fast model Groq par
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs only valid JSON matching the requested schema."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        content = completion.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        raise Exception(f"Groq API Error: {str(e)}")