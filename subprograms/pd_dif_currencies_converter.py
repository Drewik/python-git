import pandas as pd
import numpy as np

exchange = pd.read_csv("../exchange_data.csv")
currencies = list(exchange.head())
currencies.remove('date')
currencies.append('RUR')

df = pd.read_csv("vacancies_dif_currencies.csv", encoding='utf-8')


def get_multiplier(date, currency):
    if currency == 'RUR':
        return 1
    else:
        return exchange[exchange['date'] == date][currency].values[0]


df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)

df2 = df.copy()
currencies_set = set(currencies)

df2['salary'] = df2.apply(lambda x: x['salary'] \
    if (x['salary_currency'] == 'RUR' or pd.isna(x['salary']) or x['salary_currency'] not in currencies_set) \
    else (x['salary'] * get_multiplier(x['published_at'][:7], x['salary_currency'])), axis=1)

df2 = df2[['name', 'salary', 'area_name', 'published_at']]
df2['salary'] = np.floor(df2['salary'])

df2.to_csv('vacancies_dif_currencies_with_salary.csv', encoding='utf-8', index=False)
