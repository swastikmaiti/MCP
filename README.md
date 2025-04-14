 MCP
Model Context Protocol

# 🧩 MCP Agent with Web Search Integration
This project demonstrates how to build an intelligent AI assistant using LlamaIndex, FastMCP, and OpenAI's GPT-4o, enhanced with real-time web search capabilities via Serper API.

With this setup:

You can interact with an agent that answers your queries.

If needed, the agent fetches fresh data from the internet to provide accurate and up-to-date information.

## Note:
This project uses uv (a faster Python package manager) instead of pip for dependency management.

# Features
✅ AI Assistant powered by OpenAI gpt-4o

✅ Integrated with llama-index Function Agent

✅ Real-time Web Search using Serper.dev

✅ Async-first implementation for speed 🚀

✅ Custom MCP server and client communication

✅ Clean streaming of tool calls and responses

# 🧩 Tech Stack
- Python 3.11+

- uv (Python dependency management)

- FastMCP

- LlamaIndex

- OpenAI GPT-4o

- HTTPx (for async HTTP requests)

- Serper.dev API (Google Search API)

- BeautifulSoup (Web scraping)


## 📖 References

- **Server-side code reference:**  
  [MCP Quickstart Server](https://modelcontextprotocol.io/quickstart/server)

- **Client-side code reference:**  
  [LlamaIndex MCP Integration Example](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-mcp/examples/mcp.ipynb)



## 🚀 Running the Project

### 1. Start MCP Server

```bash
uv run mcp_server.py --server_type=sse
```

### 2. Start MCP Client

```bash
python mcp_client.py
```

### 3. Usage Example

```bash
You: Who is the CEO of OpenAI?
Agent: Sam Altman is the CEO of OpenAI. (retrieved from latest web search)
```
