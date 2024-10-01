FROM python:3.9.20-alpine3.20

WORKDIR /code

RUN python3 -m pip install -U discord.py