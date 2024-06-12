FROM python:3.12-slim

COPY . /app
WORKDIR /app
RUN mkdir -p /app/logs
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]


