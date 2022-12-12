import pickle
import pandas as pd
# Данные за 09.12.2022
# Сохранил их чтобы лишний раз не нагружать HH.ru
with open('vacancies_hh.pickle', 'rb') as f:
    vacancies = pickle.load(f)
    formatted_vacancies = []
    for vacancy in vacancies:
        formatted_vacancy = {}
        formatted_vacancy['name'] = vacancy.get('name')
        if vacancy['salary'] is None:
            formatted_vacancy['salary_from'] = None
            formatted_vacancy['salary_to'] = None
            formatted_vacancy['salary_currency'] = None
        else:
            formatted_vacancy['salary_from'] = vacancy['salary'].get('from')
            formatted_vacancy['salary_to'] = vacancy['salary'].get('to')
            formatted_vacancy['salary_currency'] = vacancy['salary'].get('currency')
        formatted_vacancy['area_name'] = vacancy['area'].get('name')
        formatted_vacancy['published_at'] = vacancy.get('published_at')
        formatted_vacancies.append(formatted_vacancy)
    
    df = pd.DataFrame(formatted_vacancies)
    
    df.to_csv('vacancies_hh.csv', index=False, encoding='utf-8-sig')
    

        

