FROM python:3.11-slim
LABEL maintainer="曾绍强 23110941038"
LABEL description="反欺诈检测平台"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
