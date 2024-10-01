FROM python:3.9.20-alpine3.20

WORKDIR /code

# vulnerability fix
RUN python3 -m pip install --upgrade pip==23.3 setuptools==70.0.0

# discord.py installation
RUN python3 -m pip install -U discord.py