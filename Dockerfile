FROM python:3.10-slim

# Step 1: Work directory set karein
WORKDIR /usr/src/app

# Step 2: GitHub ki sari files (chahe bahar hon ya folder mein) yahan copy karein
COPY . .

# Step 3: Zaroori libraries install karein
RUN pip install --no-cache-dir requests fake-useragent

# Step 4: System ko batana ke bot.py kahan mil sakti hai
# Hum ne ./bot.py aur ./App/bot.py dono raaste khule rakhe hain
CMD ["sh", "-c", "python bot.py || python App/bot.py"]
