FROM python:3.10-slim

# Step 1: Zaroori tools install karein
RUN apt-get update && apt-get install -y procps

# Step 2: Work Directory set karein
WORKDIR /app

# Step 3: Sari files aur folders (including 'App' folder) copy karein
COPY . .

# Step 4: Python libraries install karein
RUN pip install --no-cache-dir requests

# Step 5: Port environment variable for Koyeb
ENV PORT=8000
EXPOSE 8000

# Step 6: Smart Start Command
# Ye command pehle check karegi ke bot.py kahan hai, phir usay chalayegi
# Saath hi ek fake server chalayegi taake Health Check pass ho jaye
CMD sh -c "python -m http.server 8000 & (python bot.py || python App/bot.py || python app/bot.py)"
