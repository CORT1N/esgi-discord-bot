from data_processing import get_subjects_by_year, get_students_from_xlsx
# from discord_processing import init_channels_by_year, reset_channels_by_year, invite_students

import discord
import os

from actions import do

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GENERAL_CHANNEL_ID = int(os.getenv('DISCORD_GENERAL_CHANNEL_ID'))

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} logged in.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Commands in actions.py
    if message.content.startswith('!'):
        await do(message)
            
# @bot.event
# async def on_member_join(member):
#     check_for_role_on_join(member)

bot.run(DISCORD_TOKEN)