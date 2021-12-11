FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r \
    requirements.txt

COPY src /usr/src/app/

# CMD [ "python", "-u", "main.py" ]
