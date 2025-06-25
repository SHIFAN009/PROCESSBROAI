from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
import openai
import os

app = FastAPI()

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "FlowMind is running ✅"}

@app.post("/webhook", response_class=PlainTextResponse)
async def webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    print(f"📥 Message from {From}: {Body}")

    # Use OpenAI to generate a reply
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI for chemical and process engineering students."},
                {"role": "user", "content": Body}
            ]
        )

        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "⚠️ Sorry, I couldn't generate a response right now."

    return reply
