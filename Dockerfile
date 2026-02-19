FROM python:3.10-slim

# Step 1: Install system dependencies
RUN apt-get update && apt-get install -y procps netcat-openbsd

# Step 2: Set work directory
WORKDIR /app

# Step 3: Copy all files (including App folder if exists)
COPY . .

# Step 4: Install Python libraries
RUN pip install --no-cache-dir requests

# Step 5: Port environment variable
ENV PORT=8000
EXPOSE 8000

# Step 6: Smart Start Command
# 1. Start a simple HTTP server on port 8000 (FAST)
# 2. Wait 2 seconds
# 3. Start the bot in the background
CMD sh -c "python3 -m http.server 8000 & sleep 2 && (python3 bot.py || python3 App/bot.py)"
