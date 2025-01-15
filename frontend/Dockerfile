FROM python:3.10-slim

WORKDIR /app
COPY . /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8003
CMD ["streamlit", "run", "app.py", "--server.port=8003", "--server.address=0.0.0.0"]
