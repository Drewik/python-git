a = 0
program = input("Введите название программы (Вакансии или Статистика): ")
if program == "Вакансии":
    import subprograms.table
elif program == "Статистика":
    import subprograms.vacancies