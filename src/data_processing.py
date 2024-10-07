from openpyxl import load_workbook
import os

def get_subjects_by_year():
    WB_PATH = os.getenv('SUBJECTS_FILE_PATH')
    wb =  load_workbook(filename=WB_PATH, read_only=True)
    subjects_by_year = {}
    for sheet in wb:
        year_of_study = sheet.title
        subjects = []
        for row in sheet.iter_rows(min_row=1):
            subject = row[0].value
            if subject:
                subjects.append(subject)
        subjects_by_year[year_of_study] = subjects
    # Debug 
    for year_of_study, subjects in subjects_by_year.items():
        print(f"Year of study: {year_of_study}")
        print("Subjects:")
        for subject in subjects:
            print(f"- {subject}")
    return subjects_by_year