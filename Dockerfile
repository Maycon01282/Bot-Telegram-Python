FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /webapps/chat-bot-telegram

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libsqlite3-dev \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*  # Clean up the apt cache to reduce image size

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "bot_script.py"]
