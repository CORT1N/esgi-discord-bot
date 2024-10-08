import discord

async def init_subjects_by_year(subjects_by_year, message):
    for year_of_study, subjects in subjects_by_year.items():
        # print(f"Year of study: {year_of_study}")
        if not any(category.name == year_of_study for category in message.guild.categories):
            category = await message.guild.create_category(year_of_study)
        for subject in subjects:
            # print(f"- Subject : {subject}")
            await message.guild.create_text_channel(name=subject, category=category)
            
# async def reset_subjects_by_year(subjects_by_year, message):
#     for year_of_study, subjects in subjects_by_year.items():
#         if 
        

            

        
        # print("Subjects:")
        # for subject in subjects:
        #     print(f"- {subject}")

            
# for category in message.guild.categories:
#                 print(category.name)