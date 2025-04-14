import asyncio
import dotenv
from llama_index.llms.openai import OpenAI
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult, ToolCall
from llama_index.core.workflow import Context

# Load environment variables
dotenv.load_dotenv()

# Load LLM
llm = OpenAI(model="gpt-4o")

# System prompt for the agent
SYSTEM_PROMPT = """
You are an intelligent AI assistant designed to help users by answering their queries accurately and efficiently.

You have access to an Internet search tool to gather information when needed.

Guidelines:
- Carefully consider the user query before making a search.
- Perform at most one search per user query. Avoid making multiple or unnecessary search calls.
- Use the search tool only when you genuinely need up-to-date or external information.
- Provide clear, concise, and helpful responses to the user.
"""


async def build_agent_and_context() -> tuple[FunctionAgent, Context]:
    """Initializes the MCP client, tool spec, agent, and agent context."""
    mcp_client = BasicMCPClient("http://127.0.0.1:3000/sse")
    mcp_tool = McpToolSpec(client=mcp_client)

    agent = await get_agent(mcp_tool)
    agent_context = Context(agent)

    return agent, agent_context


async def get_agent(tools: McpToolSpec) -> FunctionAgent:
    """Creates a FunctionAgent with the given tools."""
    tool_list = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent",
        description="An agent that can perform tool calling.",
        tools=tool_list,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


async def handle_user_message(
    message_content: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = False,
) -> str:
    """Handles user input by passing it to the agent and streaming events."""
    handler = agent.run(message_content, ctx=agent_context)

    async for event in handler.stream_events():
        if verbose:
            if isinstance(event, ToolCall):
                print(f"Calling tool '{event.tool_name}' with kwargs: {event.tool_kwargs}")
            elif isinstance(event, ToolCallResult):
                print(f"Tool '{event.tool_name}' returned: {event.tool_output}")

    response = await handler
    return str(response)


async def start_interaction_loop(agent: FunctionAgent, agent_context: Context):
    """Starts the interaction loop with the user."""
    print("Agent is ready! Type your message, or 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Exiting. Goodbye!")
            break

        response = await handle_user_message(user_input, agent, agent_context, verbose=True)
        print(f"Agent: {response}\n")


async def main():
    # Build agent and context
    agent, agent_context = await build_agent_and_context()

    # Start the interaction loop
    await start_interaction_loop(agent, agent_context)


if __name__ == "__main__":
    asyncio.run(main())
