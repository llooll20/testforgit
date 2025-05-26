from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.intent import classify_intent
from agents.groupchat import intent_to_groupchat

app = FastAPI()


@app.post("/execute")
async def execute_prompt(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()

    if not prompt:
        return JSONResponse(content={"error": "Empty prompt"}, status_code=400)

    intent = classify_intent(prompt)
    if intent == "unknown":
        return JSONResponse(content={"error": "Intent not recognized"}, status_code=400)

    groupchat = intent_to_groupchat.get(intent)
    if not groupchat:
        return JSONResponse(content={"error": "Something went wrong"}, status_code=400)

    result = groupchat.run_chat(prompt)
    code = result.chat_history[-1]["content"]

    return JSONResponse(content={"code": code})
