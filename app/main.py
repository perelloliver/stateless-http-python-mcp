from mcp.server.fastmcp import FastMCP
from fastapi import Request
from starlette.responses import JSONResponse
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the MCP server

mcp = FastMCP(
    name="Test",
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",    # mount at root
    require_accept_header=False,
)

# Random tool
@mcp.tool(description="Hello world")
def hello_world(name: str = "World") -> str:
    return f"Hello, {name}!"

# Health check endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "ok"})

# Instantiate the Starlette app
app = mcp.streamable_http_app()

# Run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")