FROM python:3.9.20-alpine3.20

WORKDIR /usr/src/app

# vulnerability fix
RUN python3 -m pip install --upgrade pip==23.3 setuptools==70.0.0

# discord.py installation
RUN python3 -m pip install -U discord.py

# copying bot scripts
COPY ./bot .

# launching the bot
CMD ["python3", "-u", "main.py"]