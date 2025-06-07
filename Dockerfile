FROM python:3.8-slim

# Create a directory for the app
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Use Docker secrets
RUN --mount=type=secret,id=api_key \
    export API_KEY=$(cat /run/secrets/api_key) && \
    echo "API Key is set"

CMD ["python", "main.py"]
