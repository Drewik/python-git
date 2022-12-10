import pandas as pd
dt = pd.read_csv("vacancies_dif_currencies.csv")
print(dt["salary_currency"].value_counts())