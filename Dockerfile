FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir requests
# Koyeb worker mode configuration
ENV PORT=8080
CMD ["sh", "-c", "python bot.py || python App/bot.py"]
