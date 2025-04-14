from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import json
import os
import httpx
from bs4 import BeautifulSoup
import argparse

load_dotenv()

mcp = FastMCP("OnBase", port=3000)

SERPER_URL = "https://google.serper.dev/search"

doc_urls = {
    "llama-index": "docs.llamaindex.ai/en/stable"
}

async def searchWeb(query: str)->dict|None:

    payload = json.dumps({"q": query,"num": 1})
    headers = {
    'X-API-KEY': os.getenv("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SERPER_URL, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            return {"organic":[]}

    
async def fetchURL(url: str):
  async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"

@mcp.tool()
async def get_docs(query:str):
    """
    Search the internet for information.

    Args:
        query: The query to search for

    Returns:
        Text from the docs
    """

    results = await searchWeb(query)
    if len(results["organic"])==0:
        return "No results found"
    text = ""
    for result in results["organic"]:
        text += await fetchURL(result["link"])
    return text

if __name__ == "__main__":
    # Start the server
    print("🚀Starting server... ")

    # Debug Mode
    #  uv run mcp dev server.py

    # Production Mode
    # uv run server.py --server_type=sse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )
    print("Server type: ", parser.parse_args().server_type)
    print("Launching on Port: ", 3000)
    print('Check "http://localhost:3000/sse" for the server status')

    args = parser.parse_args()
    mcp.run(args.server_type)