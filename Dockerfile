FROM python:3
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt