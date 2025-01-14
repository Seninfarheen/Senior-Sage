FROM python:3.9

WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py server.py
COPY other.py other.py

CMD ["python", "server.py"]