def init_subjects_by_year(subjects_by_year){
    for year_of_study, subjects in subjects_by_year.items():
        print(f"Year of study: {year_of_study}")
        print("Subjects:")
        for subject in subjects:
            print(f"- {subject}")
}