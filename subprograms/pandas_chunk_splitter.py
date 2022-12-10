import pandas as pd

dt = pd.read_csv("vacancies_dif_currencies.csv")


def split_years(dt):
    return [dt[dt['published_at'].str[:4] == y] for y in dt['published_at'].str[:4].unique()]


res = split_years(dt)
for df in res:
    df.to_csv("./dif_currencies_chunks/" + df['published_at'].iat[0][:4] + ".csv", encoding='utf-8', index=False)
