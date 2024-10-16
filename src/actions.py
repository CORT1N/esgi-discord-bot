import os

from data_processing import get_subjects_by_year
from discord_processing import init_channels_by_year, reset_channels_by_year, reset_roles_by_year

DISCORD_ADMIN_ROLE_ID = os.getenv('DISCORD_ADMIN_ROLE_ID')
SUBJECTS_FILE_PATH = os.getenv('SUBJECTS_FILE_PATH')
OLD_SUBJECTS_FILE_PATH = os.getenv('OLD_SUBJECTS_FILE_PATH')

subjects_by_year = get_subjects_by_year(SUBJECTS_FILE_PATH)
old_subjects_by_year = get_subjects_by_year(OLD_SUBJECTS_FILE_PATH)

async def do(command):
    if command.content == '!init_channels_by_year' and as_permissions(command):
        await init_channels_by_year(subjects_by_year, command)
    
    if command.content == '!reset_channels_by_year' and as_permissions(command):
        await reset_channels_by_year(old_subjects_by_year, command)

    if command.content == '!reset_roles_by_year' and as_permissions(command):
        await reset_roles_by_year(old_subjects_by_year, command)
            
# Checks for admin permissions based on admin role id in env values
def as_permissions(command):
    if any(str(role.id) == DISCORD_ADMIN_ROLE_ID for role in command.author.roles):
        return True
    else:
        return False