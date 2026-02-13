# Step 1: Use Python official image
FROM python:3.9-slim

# Step 2: Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    librandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set working directory
WORKDIR /app

# Step 4: Copy files
COPY . .

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Install Playwright and Chromium browser
RUN pip install playwright && playwright install chromium

# Step 7: Expose port and run
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
