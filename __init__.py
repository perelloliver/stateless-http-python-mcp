from fastapi import FastAPI, Request, HTTPException
from starlette.responses import StreamingResponse, JSONResponse
import uvicorn

# Hypothetical Python SDK imports—adjust if package paths differ
from modelcontextprotocol.sdk.server import McpServer
from modelcontextprotocol.sdk.server.streamable_http import StreamableHTTPServerTransport

# Create a stateless MCP server factory

def get_server():
    server = McpServer(
        name="stateless-mcp-server-template",
        version="0.1.0",
    )
    # Register your prompts, resources, and tools
    from prompts import register_prompts
    from resources import register_resources
    from tools import register_tools

    register_prompts(server)
    register_resources(server)
    register_tools(server)

    # For stateful logic later, swap in Redis or API-backed state
    return server

app = FastAPI()

async def handle_mcp(request: Request):
    server = get_server()
    transport = StreamableHTTPServerTransport(session_id_generator=None)
    await server.connect(transport)

    body = await request.body()

    # streaming generator that yields chunks from the transport
    async def streamer():
        try:
            # The transport writes into the streamer via async yield
            async for chunk in transport.handle_request(request, body):
                yield chunk
        finally:
            transport.close()
            server.close()

    return StreamingResponse(
        streamer(),
        media_type="application/json"
    )

# Two POST routes: "/" and "/mcp"
app.post("/", "/mcp")(handle_mcp)
# app.post("/mcp")(handle_mcp)

# Disallow GET and DELETE on /mcp
@app.get("/mcp")
def get_not_allowed():
    raise HTTPException(status_code=405, detail={
        "jsonrpc": "2.0",
        "error": {"code": -32000, "message": "Method not allowed."},
        "id": None,
    })

@app.delete("/mcp")
def delete_not_allowed():
    raise HTTPException(status_code=405, detail={
        "jsonrpc": "2.0",
        "error": {"code": -32000, "message": "Method not allowed."},
        "id": None,
    })

if __name__ == "__main__":
    # Bind to 0.0.0.0 on PORT env or 3000
    import os
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("mcp_server:app", host="0.0.0.0", port=port, log_level="info")
