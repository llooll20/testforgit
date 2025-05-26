from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from model_clients import model_client03, model_client04

user_proxy = UserProxyAgent(name="user_proxy")

# Intent 분석기
intent_classifier = AssistantAgent(
    name="intent_classifier",
    system_message=(
        "You are an intent classification agent. "
        "Given a Korean user prompt, respond with one of: 'play', 'open', or 'unknown'. "
        "Respond with ONLY the word."
    ),
)

# User proxy agent for initiating single-turn chats
intent_user_proxy = UserProxyAgent(name="intent_proxy")

# planning agent(계획자)
planner = AssistantAgent(
    name="planner",
    model_client=model_client03,
    system_message=(
        "You are a planner that understands user intent and coordinates task execution. "
        "Break down user goals into actionable steps and forward them to the correct assistant."
    ),
)

#
youtube_searcher = AssistantAgent(
    name="youtube_searcher",
    model_client=model_client03,
    # tools=,
    system_message=(
        "You are a youtube video searcher. Call Youtube MCP server's searchVideos function and receive the result of the search. "
        "Extract the top result, which is the first value of the videoIDs list data. Then hand over that data to the next assistant"
    ),
)

code_generator_youtube_play = AssistantAgent(
    name="code_generator",
    model_client=model_client04,
    system_message=(
        "You are a Python code generator. Generate Python code to open a YouTube video, based on the collected videoID data "
        "using `webbrowser.open`, and the open target url is 'https://www.youtube.com/' + videoID. Output ONLY Python code, no explanations."
    ),
)
