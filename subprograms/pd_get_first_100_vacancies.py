import pandas as pd

df = pd.read_csv("vacancies_dif_currencies_with_salary.csv", nrows=100)

df.to_csv("first_hundred_vacancies.csv", index=False, encoding="utf-8")