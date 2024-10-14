from data_processing import get_subjects_by_year, get_students_from_xlsx
from discord_processing import init_channels_by_year, reset_channels_by_year, invite_students

import discord
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ADMIN_ROLE_ID = int(os.getenv('DISCORD_ADMIN_ROLE_ID'))
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

    if message.content.startswith('$init_year'):
        if any(role.id == DISCORD_ADMIN_ROLE_ID for role in message.author.roles):
            subjects_by_year = get_subjects_by_year(os.getenv('SUBJECTS_FILE_PATH'))
            await init_channels_by_year(subjects_by_year, message)

    if message.content.startswith('$reset_year'):
        if any(role.id == DISCORD_ADMIN_ROLE_ID for role in message.author.roles):
            subjects_by_year = get_subjects_by_year(os.getenv('OLD_SUBJECTS_FILE_PATH'))
            await reset_channels_by_year(subjects_by_year, message)

    if message.content.startswith('$invite_students'):
        if any(role.id == DISCORD_ADMIN_ROLE_ID for role in message.author.roles):
            students = get_students_from_xlsx(os.getenv('STUDENTS_FILE_PATH'))
            general_channel = bot.get_channel(DISCORD_GENERAL_CHANNEL_ID)
            await invite_students(students, general_channel)
            
# @bot.event
# async def on_member_join(member):
#     check_for_role_on_join(member)

bot.run(DISCORD_TOKEN)