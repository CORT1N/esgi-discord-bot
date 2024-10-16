from data_processing import get_db, save_db

import discord
import os

DISCORD_TEACHING_MANAGER_ROLE_ID = int(os.getenv('DISCORD_TEACHING_MANAGER_ROLE_ID'))
DISCORD_TEACHER_ROLE_ID = int(os.getenv('DISCORD_TEACHER_ROLE_ID'))
            
async def init_role_by_year(year_of_study, message):
    role = next((role for role in message.guild.roles if role.name == year_of_study), None)
    if role is None:
        role = await message.guild.create_role(
            name=year_of_study,
            hoist=True,
            colour=discord.Colour.from_str("#00ffff"),
            permissions=discord.Permissions(
                view_channel=True,
                create_instant_invite=True,
                send_messages=True,
                send_messages_in_threads=True,
                create_public_threads=True,
                embed_links=True,
                attach_files=True,
                add_reactions=True,
                use_external_emojis=True,
                use_external_stickers=True,
                connect=True, speak=True,
                stream=True,
                use_voice_activation=True,
                use_application_commands=True,
                use_embedded_activities=True
            )
        )
    return role

async def debug_init_roles_by_year(subjects_by_year, message):
    for year_of_study, subjects in subjects_by_year.items():
        await init_role_by_year(year_of_study, message)

async def reset_roles_by_year(old_subjects_by_year, message):
    for year_of_study, subjects in old_subjects_by_year.items():
        role = next((role for role in message.guild.roles if role.name == year_of_study), None)
        if role is not None:
            await role.delete()
            
async def init_category_by_year(year_of_study, role, message):
    teaching_manager_role = next((role for role in message.guild.roles if role.id == DISCORD_TEACHING_MANAGER_ROLE_ID), None)
    teacher_role = next((role for role in message.guild.roles if role.id == DISCORD_TEACHER_ROLE_ID), None)

    category = next((category for category in message.guild.categories if category.name == year_of_study), None)
    if category is None:
        category = await message.guild.create_category(
            year_of_study,
            overwrites={
                message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                role: discord.PermissionOverwrite(view_channel=True),
                teaching_manager_role: discord.PermissionOverwrite(view_channel=True),
                teacher_role: discord.PermissionOverwrite(view_channel=True)
            }
        )
    return category

async def init_channels_by_year(subjects_by_year, message):    
    for year_of_study, subjects in subjects_by_year.items():
        role = await init_role_by_year(year_of_study, message)
        category = await init_category_by_year(year_of_study, role, message)
        await init_common_channel_in_category(category, os.getenv('DISCORD_GENERAL_BY_CLASS_CHANNEL_NAME'))
        await init_private_channel_in_category(
            category,
            os.getenv('DISCORD_WITHOUT_TEACHER_BY_CLASS_CHANNEL_NAME'),
            role,
            message
        )
        for subject in subjects:
            await init_common_channel_in_category(category, subject)
        await init_voice_channels_in_category(category)
        
async def reset_channels_by_year(old_subjects_by_year, message):
    for year_of_study, subjects in old_subjects_by_year.items():
        category = next((category for category in message.guild.categories if category.name == year_of_study), None)
        if category is not None:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
        
async def init_common_channel_in_category(category, channel_name):
    channel = next((channel for channel in category.channels if channel.name == channel_name), None)
    if channel is None:
        channel = await category.create_text_channel(channel_name)
    else:
        await channel.purge()
    return channel

async def init_private_channel_in_category(category, channel_name, role, message):
    teaching_manager_role = next((role for role in message.guild.roles if role.id == DISCORD_TEACHING_MANAGER_ROLE_ID), None)
    teacher_role = next((role for role in message.guild.roles if role.id == DISCORD_TEACHER_ROLE_ID), None)
    
    channel = next((channel for channel in category.channels if channel.name == channel_name), None)
    if channel is None:
        channel = await category.create_text_channel(
            channel_name,
            overwrites={
                message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                role: discord.PermissionOverwrite(view_channel=True),
                teaching_manager_role: discord.PermissionOverwrite(view_channel=False),
                teacher_role: discord.PermissionOverwrite(view_channel=False)
            }
            )
    else:
        await channel.purge()
    return channel

async def init_voice_channels_in_category(category):
    for i in range(1,4):
        await category.create_voice_channel(f"Room {i}")

# async def invite_students(students, general_channel):
#     db = get_db()
#     for student in students:
#         invitation = await general_channel.create_invite(max_uses=1)
#         # Debug
#         print(f"Invitation to {student['last_name']} {student['first_name']} : {invitation}")
#         db[invitation.code] = {
#             'mail': student['mail'],
#             'promotion': student['promotion'],
#             'code': student['code'],
#             'member_id': ''
#         }
#     save_db(db)

# async def check_for_role_on_join(student):
