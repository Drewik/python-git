
import sqlite3
import pandas as pd
import os
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "sqlite_database.db"))
vacancy_name = input("Введите название вакансии: ")
conn.execute('delete from vacancies_dif_currencies_salary where salary is null')
vacancies_average_salary_by_year = pd.read_sql('select substr(published_at, 0, 5) as "year", round(avg(salary)) as "average_salary" from vacancies_dif_currencies_salary group by year', conn)
vacancies_count_by_year = pd.read_sql('select substr(published_at, 0, 5) as "year", count(*) as "count" from vacancies_dif_currencies_salary group by year', conn)
vacancies_count_by_year_selected_vacancy = pd.read_sql('select substr(published_at, 0, 5) as "year", count(*) as "count" from vacancies_dif_currencies_salary where name like "%'+vacancy_name+'%" group by year', conn)
vacancies_average_salary_by_year_selected_vacancy = pd.read_sql('select substr(published_at, 0, 5) as "year", round(avg(salary)) as "average_salary" from vacancies_dif_currencies_salary where name like "%'+vacancy_name+'%" group by year', conn)
number_of_vacancies = conn.execute('select count(*) from vacancies_dif_currencies_salary').fetchone()[0]
one_percent_of_vacancies = number_of_vacancies // 100
vacancies_fraction_by_city = pd.read_sql('select area_name, count(*)*1.0 / {}  as "fraction" from vacancies_dif_currencies_salary group by area_name order by fraction desc limit 10'.format(number_of_vacancies), conn)
vacancies_top_average_salary_by_city = pd.read_sql('select area_name, round(avg(salary)) as "average_salary" from vacancies_dif_currencies_salary group by area_name having count(*) > {} order by average_salary desc limit 10'.format(one_percent_of_vacancies), conn)

print("Динамика уровня зарплат по годам:")
print(vacancies_average_salary_by_year.to_string(index=False))
print("")
print("Динамика количества вакансий по годам:")
print(vacancies_count_by_year.to_string(index=False))
print("")
print("Динамика уровня зарплат по годам для выбранной профессии:")
print(vacancies_average_salary_by_year_selected_vacancy.to_string(index=False))
print("")
print("Динамика количества вакансий по годам для выбранной профессии:")
print(vacancies_count_by_year_selected_vacancy.to_string(index=False))
print("")
print("Уровень зарплат по городам (в порядке убывания):")
print(vacancies_top_average_salary_by_city.to_string(index=False))
print("")
print("Доля вакансий по городам (в порядке убывания):")
print(vacancies_fraction_by_city.to_string(index=False))
