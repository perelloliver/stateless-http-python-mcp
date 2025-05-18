Example of a lightweight, stateless HTTP-streaming MCP server with out-of-the-box Docker containerization for serverless deployment.


## Build the docker image
```
docker build -t stateless-http-python-mcp .
```

## Run the container
```
docker run --rm -it \                      
  -p 8080:8080 \
  -e PORT=8080 \
  stateless-http-python-mcp
```

## Run the inspector
```
mcp dev app/main.py
```

## Test endpoints - examples

### Health check
```
curl -i \
  -X GET "http://localhost:8080/health" \
  -H "Accept: application/json, text/event-stream"

```
### List tools
```curl -X POST "http://localhost:8080/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

### Call a tool
```
curl -X POST "http://localhost:8080/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "hello_world",
      "arguments": {"name": "YourName"}
    }
  }'
  ```
