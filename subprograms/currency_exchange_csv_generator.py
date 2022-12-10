import requests
import pandas as pd

response = requests.get("http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=01/01/2017")
currencies_to_convert = ["BYR", "USD", "EUR", "KZT", "UAH"]
print(currencies_to_convert)
df = pd.DataFrame(columns=currencies_to_convert)
exchange_data = []
for year in range(2003, 2023):
    for month in range(1, 13):
        if year == 2016 and month == 7:
            currencies_to_convert[0] = "BYN"
        date = f"01/{month:02d}/{year}"
        response = requests.get(f"http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={date}")
        if response.status_code == 200:
            exchange_xml = pd.read_xml(response.text)
            monthly_currencies = []
            monthly_currencies.append(f"{year}-{month:02d}")
            for currency in currencies_to_convert:
                monthly_currencies.append(
                    exchange_xml[exchange_xml["CharCode"] == currency]["Value"].apply(
                        lambda x: float(x.split()[0].replace(',', '.'))).values[0]
                     / exchange_xml[exchange_xml["CharCode"] == currency]["Nominal"].apply(lambda x: float(x)).values[
                         0])
            exchange_data.append(monthly_currencies)
        else:
            break
currencies_to_convert[0] = "BYR"
df = pd.DataFrame(exchange_data, columns=["date"] + currencies_to_convert)
df.to_csv("exchange_data.csv", index=False, encoding="utf-8")
