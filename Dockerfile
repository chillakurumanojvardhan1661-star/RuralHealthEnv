FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables (defaults)
ENV API_BASE_URL=https://api.openai.com/v1
ENV MODEL_NAME=gpt-4-turbo
ENV HF_TOKEN=""

# Command to run (defaults to inference)
CMD ["python", "inference.py"]
