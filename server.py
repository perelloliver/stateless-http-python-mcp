from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the MCP server
# The path for this is atypical due to how it is setup with Starlette under the hood
# Starlette adds a slash to trailing names, so we have to hit /mcp/ instead of /mcp
# Likewise, this doesn't work if we update the streamable_http_path to / because the mount is at /
# Probably an easy fix for this in the future but just leaving it here for now.

# This also doesn't work with the Inspector
# because it doesn't know how to handle the streamable_http_path
# and the default /mcp path is not a valid path for the Inspector

# Unsure if this is my mistake or a bug in the library

mcp = FastMCP(
    name="Test", 
    stateless_http=True,
    settings={
        "json_response": True,
        "streamable_http_path": "/mcp/",
        "require_accept_header": False
    }
)

# Random tool
@mcp.tool(description="Hello world")
def hello_world(name: str = "World") -> str:
    return f"Hello, {name}!"

# Health check endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "ok"})

# Get the Starlette app
app = mcp.streamable_http_app()

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)