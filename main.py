from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.intent import classify_intent
from agents.groupchat import intent_to_groupchat
from autogen_agentchat.ui import Console


def extract_final_answer(task_result):
    code_candidates = []

    for msg in task_result.messages:
        if getattr(msg, "type", None) == "TextMessage" and msg.content:
            content = msg.content.strip()
            if "#CommandCode" in content:
                break
            # Filter out JSON-looking messages
            if content.startswith("{") and content.endswith("}"):
                continue
            code_candidates.append(content)

    # Return the last collected pure code block (if any)
    return code_candidates[-1] if code_candidates else ""


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

    team = intent_to_groupchat.get(intent)
    if not team:
        return JSONResponse(
            content={"error": "No groupchat found for intent"}, status_code=500
        )

    task_result = await Console(team.run_stream(task=prompt))
    code = extract_final_answer(task_result)
    print(f"Final Command Code", {code})

    return JSONResponse(content={"code": code})
