from openpyxl import load_workbook
import os

def get_subjects_by_year():
    return arrange_subjects_from_xlsx(get_subjects_from_xlsx())

def get_subjects_from_xlsx():
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
    return subjects_by_year

def arrange_subjects_from_xlsx(subjects_by_year):
    for year_of_study, subjects in subjects_by_year.items():
        subjects = sorted(set(subject.strip()[:100] for subject in subjects))
        subjects_by_year[year_of_study] = subjects
    return subjects_by_year