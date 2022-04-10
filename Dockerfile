FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY data ./data/
COPY static ./static/
COPY templates ./templates/
COPY app.py .
COPY functions.py .

CMD flask run -h 0.0.0.0 -p 80
