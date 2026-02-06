import httpx 
from config import GEMINI_URL , GEMINI_API_KEY
async def get_gemini_response(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {"prompt": prompt, "max_tokens": 200} 

    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, json=data, headers=headers)
        response.raise_for_status()  
        result = response.json()
        return result.get("text", "") 