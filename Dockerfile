FROM mcr.microsoft.com/playwright:v1.40.0-jammy
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
