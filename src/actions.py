import os

from data_processing import get_subjects_by_year, get_students_from_xlsx
from discord_processing import *

DISCORD_ADMIN_ROLE_ID = os.getenv('DISCORD_ADMIN_ROLE_ID')
DISCORD_GENERAL_CHANNEL_ID = os.getenv('DISCORD_GENERAL_CHANNEL_ID')

SUBJECTS_FILE_PATH = os.getenv('SUBJECTS_FILE_PATH')
OLD_SUBJECTS_FILE_PATH = os.getenv('OLD_SUBJECTS_FILE_PATH')
STUDENTS_FILE_PATH = os.getenv('STUDENTS_FILE_PATH')

subjects_by_year = get_subjects_by_year(SUBJECTS_FILE_PATH)
old_subjects_by_year = get_subjects_by_year(OLD_SUBJECTS_FILE_PATH)
students = get_students_from_xlsx(STUDENTS_FILE_PATH)

async def do(command):
    # Role needed : ADMIN
    if command.content == '!init_channels_by_year' and as_permissions(command):
        await init_channels_by_year(subjects_by_year, command)
    if command.content == '!reset_channels_by_year' and as_permissions(command):
        await reset_channels_by_year(old_subjects_by_year, command)
    if command.content == '!reset_roles_by_year' and as_permissions(command):
        await reset_roles_by_year(old_subjects_by_year, command)
    if command.content == '!invite_students' and as_permissions(command):
        await create_invite_by_student(students, DISCORD_GENERAL_CHANNEL_ID, command)
    ## Debug commands
    if command.content == '!debug_init_roles_by_year' and as_permissions(command):
        await debug_init_roles_by_year(subjects_by_year, command)

# Checks for admin permissions based on admin role id in env values
def as_permissions(command):
    if any(str(role.id) == DISCORD_ADMIN_ROLE_ID for role in command.author.roles):
        return True
    else:
        return False