# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.intent import classify_intent
from agents.groupchat import intent_to_groupchat

import asyncio

app = FastAPI()

@app.post("/execute")
async def execute_prompt(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return JSONResponse(content={"error": "Empty prompt"}, status_code=400)

    intent = await classify_intent(prompt)
    if intent == "unknown":
        return JSONResponse(content={"error": "Intent not recognized"}, status_code=400)

    groupchat = intent_to_groupchat.get(intent)
    if not groupchat:
        return JSONResponse(content={"error": "No groupchat found for intent"}, status_code=500)

    # Async run
    result = await groupchat.a_run_chat(prompt)

    # Extract final agent reply
    code = result.chat_history[-1].get("content", "")

    return JSONResponse(content={"code": code})