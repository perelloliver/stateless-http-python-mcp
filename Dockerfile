FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Port
ENV PORT=8080
EXPOSE 8080

# Start the server, pointing at app/main.py’s `app` object
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
