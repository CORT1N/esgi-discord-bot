import discord
import os

### ATTENTION : If you try (maybe to debug some problems) too much, Discord Gateway will ban you 12h

async def init_subjects_by_year(subjects_by_year, message):
    DISCORD_TEACHING_MANAGER_ROLE_ID = int(os.getenv('DISCORD_TEACHING_MANAGER_ROLE_ID'))
    teaching_manager_role = next((role for role in message.guild.roles if role.id == DISCORD_TEACHING_MANAGER_ROLE_ID), None)
    DISCORD_TEACHER_ROLE_ID = int(os.getenv('DISCORD_TEACHER_ROLE_ID'))
    teacher_role = next((role for role in message.guild.roles if role.id == DISCORD_TEACHER_ROLE_ID), None)
    for year_of_study, subjects in subjects_by_year.items():
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
        await category.create_text_channel(os.getenv('DISCORD_GENERAL_BY_CLASS_CHANNEL_NAME'))
        await category.create_text_channel(
            os.getenv('DISCORD_WITHOUT_TEACHER_BY_CLASS_CHANNEL_NAME'),
            overwrites={
                message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                role: discord.PermissionOverwrite(view_channel=True),
                teaching_manager_role: discord.PermissionOverwrite(view_channel=False),
                teacher_role: discord.PermissionOverwrite(view_channel=False)
            }
        )
        for subject in subjects:
            channel = next((channel for channel in category.channels if channel.name == subject), None)
            if channel is None:
                channel = await category.create_text_channel(subject)
            else:
                await channel.purge()
        for i in range(1,4):
            await category.create_voice_channel(f"Room {i}")
        

# This function was created to debug init_subjects_by_year() when it stops before the end
async def reset_subjects_by_year(subjects_by_year, message):
    for year_of_study, subjects in subjects_by_year.items():
        category = next((category for category in message.guild.categories if category.name == year_of_study), None)
        if category is not None:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
        role = next((role for role in message.guild.roles if role.name == year_of_study), None)
        if role is not None:
            await role.delete()
        