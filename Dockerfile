FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000
CMD uvicorn src.main:app --host 0.0.0.0 --port 8000