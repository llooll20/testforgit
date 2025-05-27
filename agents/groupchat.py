from agents.registry import (
    user_proxy,
    play_planner,
    youtube_searcher,
    videoId_extractor,
    code_generator_youtube_play,
)
from agents.model_clients import model_client04
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.
"""

text_mention_termination = TextMentionTermination("#CommandDone")
max_messages_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_messages_termination

play_team_agents = [
    user_proxy,
    play_planner,
    youtube_searcher,
    videoId_extractor,
    code_generator_youtube_play,
]
# open_team_agents = [user_proxy, planner, code_generator_youtube_play]

play_team = SelectorGroupChat(
    participants=play_team_agents,
    model_client=model_client04,
    selector_prompt=selector_prompt,
    termination_condition=termination,
    # max_turns=20,
)

# open_groupchat = SelectorGroupChat(
#     participants=open_team_agents,
#     model_client=model_client04,
#     selector_prompt=selector_prompt,
#     max_turns=20,
# )

intent_to_groupchat = {
    "play": play_team,
    # "open": open_groupchat,
}
