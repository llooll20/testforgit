from agents.registry import (
    user_proxy,
    planner,
    youtube_searcher,
    code_generator_youtube_play,
)
from model_clients import model_client03, model_client04
from autogen_agentchat.teams import SelectorGroupChat

play_team_agents = [user_proxy, planner, youtube_searcher, code_generator_youtube_play]
open_team_agents = [user_proxy, planner, code_generator_youtube_play]

play_groupchat = SelectorGroupChat(
    participants=play_team_agents,
    model_client=model_client03,
    max_turns=20,
)

open_groupchat = SelectorGroupChat(
    participants=open_team_agents,
    model_client=model_client04,
    max_turns=20,
)

intent_to_groupchat = {
    "play": play_groupchat,
    "open": open_groupchat,
}
