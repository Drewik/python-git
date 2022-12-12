import pickle
import requests
import json


def iter_pages(pages, params, url, vacancies):
    for page in range(1, pages):
        params['page'] = page
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response = response.json()
            vacancies += response["items"]
        else:
            print(f'Ошибка {response.status_code} при получении данных с HH.ru')
            print(response.text)
            input("Нажмите Enter для продолжения...")
            return


def get_vacancies():
    url = 'https://api.hh.ru/vacancies'
    params = {
        'date_from': '2022-12-09T00:00:00+0300',
        'date_to': '2022-12-09T23:59:59+0300',
        'per_page': 100,
        'page': 0,
        'specialization': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response = response.json()
    else:
        print(f'Ошибка {response.status_code} при получении данных с HH.ru')
        print(response.text)
        input("Нажмите Enter для продолжения...")
        return
    vacancies = response["items"]
    pages = response["pages"]
    iter_pages(pages, params, url, vacancies)
    for i in range(2, 24, 2):
        params['date_from'] = f'2022-12-09T{i:02d}:00:00+0300'
        params['date_to'] = f'2022-12-09T{i + 1:02d}:59:59+0300'
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response = response.json()
        else:
            print(f'Ошибка {response.status_code} при получении данных с HH.ru')
            print(response.text)
            input("Нажмите Enter для продолжения...")
        pages = response["pages"]
        iter_pages(pages, params, url, vacancies)

    return vacancies


res = get_vacancies()
# pickle get_vacancies
with open('vacancies_hh.pickle', 'wb') as f:
    pickle.dump(res, f)
# json dump get_vacancies
with open('vacancies_hh_json_dump.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False)
