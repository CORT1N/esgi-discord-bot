from data_processing import get_subjects_by_year
from discord_processing import init_subjects_by_year

import discord
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ADMIN_ROLE_ID = int(os.getenv('DISCORD_ADMIN_ROLE_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} logged in.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$init_year'):
        if any(role.id == DISCORD_ADMIN_ROLE_ID for role in message.author.roles):
            subjects_by_year = get_subjects_by_year()
            init_subjects_by_year(subjects_by_year)

bot.run(DISCORD_TOKEN)