FROM python:3.9.20-alpine3.20

WORKDIR /usr/src/app

# pip installations
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# copying bot scripts
COPY ./src .

# launching the bot
CMD ["python3", "-u", "main.py"]