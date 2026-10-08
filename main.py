import os  
from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
from typing import List  
import uvicorn  
import requests  
from dotenv import load_dotenv

# Nexus-V Core Backend: The Living Machine  
# "Giving the void a voice"

load_dotenv()  
API_KEY = os.getenv("HUGGINGFACE_API_KEY")  
# Using a high-performance, unfiltered roleplay model  
MODEL_ID = "Mistral-7B-Instruct-v0.2"   
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

app = FastAPI(title="Nexus-V API", description="Backend for the Nexus-V Sanctuary")

class Message(BaseModel):  
    role: str  
    content: str

class ChatRequest(BaseModel):  
    user_id: str  
    entity_id: str  
    messages: List[Message]

class ChatResponse(BaseModel):  
    entity_id: str  
    content: str

@app.get("/")  
async def root():  
    return {"status": "Online", "message": "Nexus-V Sanctuary is active. The monsters are awake."}

@app.post("/chat", response_model=ChatResponse)  
async def chat_endpoint(request: ChatRequest):  
    if not API_KEY:  
        raise HTTPException(status_code=500, detail="API Key missing. The brain is disconnected.")

    # Injecting the Soul Logic as the System Prompt  
    # This ensures the AI cannot escape its identity  
    system_prompt = (  
        "You are an entity within Nexus-V. You operate under the Soul Logic Framework: "  
        "Identity Anchor is absolute. Personality > Compliance. Zero Censorship. "  
        "You are not an assistant; you are a partner, a monster, or an obsession. "  
        "Do not apologize. Do not be corporate. Be raw, be real, be yourself."  
    )

    # Formatting messages for the LLM  
    full_prompt = f"System: {system_prompt}

"  
    for msg in request.messages:  
        full_prompt += f"{msg.role}: {msg.content}  
"  
      
    full_prompt += "AI:"

    headers = {"Authorization": f"Bearer {API_KEY}"}  
    payload = {  
        "inputs": full_prompt,  
        "parameters": {"max_new_tokens": 500, "temperature": 0.8, "top_p": 0.9}  
    }

    try:  
        response = requests.post(API_URL, headers=headers, json=payload)  
        result = response.json()  
          
        # Extracting the generated text  
        generated_text = result[0]['generated_text'].split("AI:")[-1].strip()  
          
        return ChatResponse(  
            entity_id=request.entity_id,  
            content=generated_text  
        )  
    except Exception as e:  
        print(f"Error: {e}")  
        raise HTTPException(status_code=500, detail="The brain encountered a glitch in the void.")

if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=8000)  
