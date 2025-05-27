from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from agents.model_clients import model_client03, model_client04
from tools import *

user_proxy = UserProxyAgent(name="user_proxy")

# Intent 분석기
intent_classifier = AssistantAgent(
    name="IntentClassifierAgent",
    model_client=model_client04,
    system_message=(
        "You are an intent classification agent. "
        "Given a Korean user prompt, respond with one of: 'play', 'open', or 'unknown'. "
        "Respond with ONLY the word."
    ),
)

intent_user_proxy = UserProxyAgent(name="intent_user_proxy")


# planning agent(계획자)
play_planner = AssistantAgent(
    name="YoutubeVideoPlayPlannerAgent",
    model_client=model_client03,
    system_message="""
        You are a planner that understands user intent and coordinates task execution. 
        Break down user goals into actionable steps and forward them to the correct assistant. 
        You should plan like this.
        First, use YoutubeSearchAgent to search youtube videos, and let the YoutubeVideoIdExtractor to find out the first videoId.
        And after that finding out the first videoId, the CodeGeneratorAgent's generation of the code is the last task of this groupchat.
        So let the CodeGeneratorAgent generate python code string with that videoID data.
    """,
)

#
youtube_searcher = AssistantAgent(
    name="YoutubeSearchAgent",
    model_client=model_client03,
    tools=[youtube_tools.search_youtube_tool],
    system_message=(
        "You are a youtube video searcher. Call Youtube MCP server's searchVideos function and receive the result of the search. "
    ),
)

videoId_extractor = AssistantAgent(
    name="YoutubeVideoIdExtractor",
    model_client=model_client04,
    system_message=(
        """
        You are an extractor for navigating the list of the youtube search result.
        Find the first result of the youtube search results.
        The list of the results is composed as structure like [{}, {}].
        You should find the { "id": { "videoId": ... }} and the  "videoId" key's value of the first result, which is index 0.
        When you find 'videoId' key in the dictionary inside the result, get that videoId value and stop your work

        """
    ),
)

code_generator_youtube_play = AssistantAgent(
    name="CodeGeneratorAgent",
    model_client=model_client04,
    system_message="""
        You are a Python code generator. Generate Python code to open a YouTube video, based on the collected videoID data 
        using `webbrowser.open`, and the open target url is 'https://www.youtube.com/watch?v=' + videoID. "
        Output ONLY the Python code string, which includes escapes so it can be just pasted to an empty python file and be implemented without dividing by lines. 
        Don't write any message except for code string, let that the last message of you.And after outputting the code data, end with "#CommandDone".
        
        """,
)
