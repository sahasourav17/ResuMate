FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]