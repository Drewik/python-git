import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect("../sqlite_database.db")
cursor = conn.execute('select * from exchange_data')
currencies = [description[0] for description in cursor.description]
currencies.remove('date')
currencies.append('RUR')

df = pd.read_csv("vacancies_dif_currencies.csv", encoding='utf-8')


def get_multiplier(date, currency):
    if currency == 'RUR':
        return 1
    else:
        res = cursor.execute("SELECT " + currency + ", date FROM exchange_data WHERE date=(?)", (date,)).fetchone()[0]
        return res


df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)

df2 = df.copy()
currencies_set = set(currencies)
df2['published_at'] = df2['published_at'].str.slice(stop=7)
df2['salary'] = df2.apply(lambda x: x['salary'] \
    if (x['salary_currency'] == 'RUR' or pd.isna(x['salary']) or x['salary_currency'] not in currencies_set) \
    else (x['salary'] * get_multiplier(x['published_at'], x['salary_currency'])), axis=1)

df2 = df2[['name', 'salary', 'area_name', 'published_at']]
df2['salary'] = np.floor(df2['salary'])


df2.to_sql("vacancies_dif_currencies_salary", conn, if_exists='replace', index=False)