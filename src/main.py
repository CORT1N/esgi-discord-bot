import discord
import os

from actions import do
# from discord_processing import assign_role_on_join

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

@bot.event
async def on_member_join(member):
    print('WIP : role attribution on join')

bot.run(DISCORD_TOKEN)