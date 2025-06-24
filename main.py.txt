from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from fastapi.responses import PlainTextResponse

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    Body: str
    From: str

@app.post("/webhook")
async def whatsapp_webhook(msg: Message):
    user_msg = msg.Body

    system_prompt = (
        "You are FlowMind, an AI tutor for chemical & process engineering students. "
        "Answer like a helpful friend: short, clear, and focused. Help with solving questions, viva prep, and project ideas."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response['choices'][0]['message']['content']
    return PlainTextResponse(content=reply)
