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
    sender: str = Form(...)
):
    print(f"📨 Message from {sender}: {Body}")

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
    print("Error with OpenAI:", e)
    reply = f"a. Sorry, I couldn't generate a response right now. Error: {e}"


    return reply
