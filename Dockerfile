# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
# COPY FlaskWebsite/requirements.txt requirements.txt
RUN pip install -r requirements.txt
# COPY . .
CMD ["python", "app.py"]