from autogen_core.tools import FunctionTool
from typing_extensions import Annotated
import asyncio
import base64
import json
import mcp
from mcp.client.streamable_http import streamablehttp_client
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SMITHERY_API_KEY = os.getenv("SMITHERY_API_KEY")

# Tool function
async def search_youtube_videos(
    query: Annotated[str, "Search query for YouTube videos"]
) -> dict:
    config = {
        "youtubeApiKey": YOUTUBE_API_KEY,
        "youtubeTranscriptLang": "en"
    }
    config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
    api_key = SMITHERY_API_KEY
    url = f"https://server.smithery.ai/@icraft2170/youtube-data-mcp-server/mcp?config={config_b64}&api_key={api_key}"

    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with mcp.ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("searchVideos", {"query": query})
            return result.output


# Register the function as a FunctionTool
search_youtube_tool = FunctionTool(
    search_youtube_videos,
    name="search_youtube_videos",
    description="Searches for videos on YouTube using the MCP YouTube tool."
)