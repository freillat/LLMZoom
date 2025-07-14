from fastmcp import Client        
import asyncio

async def main():
    async with Client("weather_server.py") as mcp_client:
        print("Client connected to MCP server.")

        print("\nRequesting available tools from the server...")
        available_tools = await mcp_client.list_tools()
        print(f"Available tools: {available_tools}")

if __name__ == "__main__":
    test = asyncio.run(main())