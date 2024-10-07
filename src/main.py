from data_processing import get_subjects_by_year

import discord
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

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
        await message.channel.send('Placeholder')
        subjects_by_year = get_subjects_by_year()


bot.run(DISCORD_TOKEN)