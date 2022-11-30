import csv
import re
from datetime import datetime
from math import floor
from prettytable import PrettyTable, ALL

class DataSet:
    """ Класс для обработки входных данных в формате CSV.

    Attributes:
        file_name (str): Название файла в формате "*****.csv"
        vacancies_objects (list): Список вакансий в виде объектов обработанных csv парсером.
    """
    def universal_csv_parser(self, file_name):
        """Парсер csv файла.

        Args:
            file_name (str): Название файла в формате "*****.csv"

        Returns:
            list(dict) : Список словарей вакансий
        """
        def csv_reader(file_name):
            """Обработчик csv данных.

            Args: file_name (str): Название файла в формате "*****.csv"

            Returns:
                field_names (list(str)) : Список заголовков таблицы
                fields (list(list(str))) : Список данных
            """
            f = open(file_name, mode="r", encoding="utf-8-sig")
            reader = csv.reader(f)
            try:
                field_names = next(reader)
            except:
                return 0
            fields = []

            for row in reader:
                if len(row) < len(field_names):
                    continue
                correct_row = True
                for e in row:
                    if len(e) == 0:
                        correct_row = False
                        break
                if correct_row:
                    fields.append(row)

            return field_names, fields

        reader_data = csv_reader(file_name)
        if reader_data == 0:
            return reader_data

        naming = reader_data[0]
        fields = reader_data[1]

        def remove_html(string):
            """Убирает html из строки.

            Args:
                 string(str): Строка

            Returns:
                string: Строка, очищенная от HTML символов
            """
            regex = re.compile(r'<[^>]+>')
            return regex.sub('', string)

        def repair_string(s):
            """Убирает из строки лишние пробелы и HTML символы.

            Args:
                s (str): Строка

            Returns:
                string: Строка, без лишних пробелов и HTML символов
            """
            s = remove_html(s)
            s = s.strip()
            s = " ".join(s.split())
            return s

        def csv_filer(reader, list_naming):
            """Заполняет словарь вакансии, ключами которого являются названия входных полей.

            Args:
                list_naming (list(str)) : Список полей вакансии, полученный из заголовка таблицы
                reader (list(list(str))) : Список данных

            Returns:
                list(dict): Список словарей с ключами-заголовками list_naming и соответствующими им полями вакансии
            """
            vacancy_dictionary_list = []
            for field in reader:
                d = dict()
                for i in range(len(list_naming)):
                    field_name = list_naming[i]
                    field_string_data = field[i]
                    if field_name == "key_skills":
                        field_string_data = field_string_data.splitlines()
                        for j in range(len(field_string_data)):
                            field_string_data[j] = repair_string(field_string_data[j])
                            if list_naming[i] != "description":
                                field_string_data[j] = field_string_data[j].replace("True", "Да").replace("False",
                                                                                                          "Нет")
                    else:
                        field_string_data = repair_string(field_string_data)
                        if list_naming[i] != "description":
                            field_string_data = field_string_data.replace("True", "Да").replace("False", "Нет")
                    d[field_name] = field_string_data
                vacancy_dictionary_list.append(d)
            return vacancy_dictionary_list

        return csv_filer(fields, naming)

    def __init__(self, file_name):
        """Инициализирует Dataset, выполняет парсинг CSV файла

        Args:
            file_name (str): Название файла в формате "*****.csv"
        """
        self.file_name = file_name
        self.vacancies_dicts = self.universal_csv_parser(file_name)
        if isinstance(self.vacancies_dicts, list):
            self.vacancies_objects = [Vacancy(d) for d in self.vacancies_dicts]


class Salary:
    """Класс для представления зарплаты.

    Attributes:
        salary_from (int or float or str): Нижняя граница вилки оклада
        salary_to (int or float or str): Верхняя граница вилки оклада
        salary_currency (str): Валюта оклада
        currency_to_rub (dict): Словарь конвертации валюты
        rub_salary (float): Средняя зарплата (float), переведенная в рубли с помощью словаря currency_to_rub
    """
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, vacancy_dictionary):
        """Инициализирует объект Salary, выполняет конвертацию для целочисленных полей.

        Args:
            vacancy_dictionary (dict(str)) : Словарь вакансии, включающий в себя пары ключ-значения зарплаты
        """
        self.salary_from = vacancy_dictionary["salary_from"]
        self.salary_to = vacancy_dictionary["salary_to"]
        self.salary_gross = vacancy_dictionary["salary_gross"].replace("Нет", "False").replace("Да", "True")
        self.salary_currency = vacancy_dictionary["salary_currency"]

    @property
    def rub_salary(self):
        """Вычисляет среднюю зарплату и переводит в рубли, при помощи словаря currency_to_rub.

        Returns:
            float: Средняя зарплата в рублях
        """
        return floor((float(self.salary_from) * self.currency_to_rub[self.salary_currency]
                      + float(self.salary_to) * self.currency_to_rub[self.salary_currency])
                     / 2)


class Vacancy:
    """Класс для хранения данных о вакансии.

    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (str): Навыки
        experience_id (str): Опыт работы
        premium (str): Премиум вакансия
        employer_name (str): Компания
        salary (float): Зарплата в рублях
        area_name (str): Город
        published_at (str): Дата публикации вакансии
    """
    def __init__(self, vacancy_dictionary):
        """Иницилиазирует объект Vacancy из словаря vacancy_dictionary.

        Args:
            vacancy_dictionary (dict): Словарь с исходными данными о вакансии
        """
        self.name = vacancy_dictionary["name"]
        self.description = vacancy_dictionary["description"]
        self.key_skills = vacancy_dictionary["key_skills"]
        self.experience_id = vacancy_dictionary["experience_id"]
        self.premium = vacancy_dictionary["premium"].replace("Нет", "False").replace("Да", "True")
        self.employer_name = vacancy_dictionary["employer_name"]
        self.salary = Salary(vacancy_dictionary)
        self.area_name = vacancy_dictionary["area_name"]
        self.published_at = vacancy_dictionary["published_at"]


class InputConnect:
    """Отвечает за обработку параметров вводимых пользователем:
    фильтры, сортировка, диапазон вывода, требуемые столбцы,
    а также за печать таблицы на экран

    Attributes:
        file_name (str) : Название файла
        vacancy_contains (str) : Параметр фильтрации
        sortby (str) : Параметр сортировки
        sort_order (str): Обратный порядок сортировки (Да / Нет)
        vacancy_range (str or int) : Диапазон вывода вакансий
        headers (str) : Требуемые стоблцы таблицы
    """
    eng_rus_conversion = {
        "name": "Название",
        "description": "Описание",
        "key_skills": "Навыки",
        "experience_id": "Опыт работы",
        "premium": "Премиум-вакансия",
        "employer_name": "Компания",
        "salary": "Оклад",
        "area_name": "Название региона",
        "published_at": "Дата публикации вакансии",
    }
    rus_eng_conversion = {
        "Название": "name",
        "description": "Описание",
        "Навыки": "key_skills",
        "Опыт работы": "experience_id",
        "Премиум-вакансия": "premium",
        "Компания": "employer_name",
        "Оклад": "salary",
        "Название региона": "area_name",
        "Дата публикации вакансии": "published_at",
        "Идентификатор валюты оклада": "salary_currency",
    }

    def __init__(self, file_name, vacancy_contains, sortby, sort_order, vacancy_range, headers):
        """Обработка инициализируемых пользователем параметров

        Args:
            file_name (str) : Название файла
            vacancy_contains (str) : Параметр фильтрации
            sortby (str) : Параметр сортировки
            sort_order (str): Обратный порядок сортировки (Да / Нет)
            vacancy_range (Union[str, int]) : Диапазон вывода вакансий
            headers (list(str)) : Требуемые стоблцы таблицы
        """
        if sortby not in self.rus_eng_conversion and sortby != "":
            print("Параметр сортировки некорректен")
            exit()
        if sort_order != "Да" and sort_order != "Нет" and sort_order != "":
            print("Порядок сортировки задан некорректно")
            exit()
        if ":" not in vacancy_contains and vacancy_contains != "":
            print("Формат ввода некорректен")
            exit()
        split_filter = vacancy_contains.split(": ")
        ru_filter = split_filter[0]
        if ru_filter not in self.rus_eng_conversion and ru_filter != "":
            print("Параметр поиска некорректен")
            exit()
        self.file_name = file_name
        self.vacancy_contains = vacancy_contains
        self.vacancies_sortby = sortby
        self.vacanies_sort_order = sort_order
        self.vacancy_range = vacancy_range
        self.headers = headers

    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }
    experience_conversion = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"
    }
    experience_order = {
        "noExperience": 0,
        "between1And3": 1,
        "between3And6": 2,
        "moreThan6": 3,
    }
    currency_conversion = {
        "AZN": "Манаты",
        "BYR": "Белорусские рубли",
        "EUR": "Евро",
        "GEL": "Грузинский лари",
        "KGS": "Киргизский сом",
        "KZT": "Тенге",
        "RUR": "Рубли",
        "UAH": "Гривны",
        "USD": "Доллары",
        "UZS": "Узбекский сум",
    }
    experience_conversion_reversed = {v: k for k, v in experience_conversion.items()}
    currency_conversion_reversed = {v: k for k, v in currency_conversion.items()}

    def parser_decorator(self, dataset):
        """Декоратор, который  применяет к ним соответствующие функции по русскоязычным подстановкам из словарей,
         фильтрации данных, сортировки данных и вывода данных."""
        def sorter(sortby, sort_order, vacancy_dictionary_list):
            """Сортирует словарь вакансий по выбранным параметрам

            Args:
                sortby (str) : Параметр сортировки
                sort_order (str): Обратный порядок сортировки (Да / Нет)

            Returns:
                list(dict): отсортированный словарь вакансий
            """
            if sortby == "":
                return vacancy_dictionary_list

            bool_sort_order = False
            if sort_order == "Да":
                bool_sort_order = True
            if sortby == "Навыки":
                vacancy_dictionary_list.sort(key=lambda x: len(x[self.rus_eng_conversion["Навыки"]]),
                                             reverse=bool_sort_order)
                return vacancy_dictionary_list
            elif sortby == "Оклад":
                vacancy_dictionary_list.sort(
                    key=lambda x: (
                        floor((float((x['salary_from'])
                                     if x["salary_currency"] == "RUR"
                                     else float(x['salary_from']) * self.currency_to_rub[x["salary_currency"]])
                               + float((x['salary_to'])
                                       if x["salary_currency"] == "RUR"
                                       else float(x['salary_to']) * self.currency_to_rub[x["salary_currency"]])) / 2)),
                    reverse=bool_sort_order)
                return vacancy_dictionary_list
            elif sortby == "Дата публикации вакансии":
                vacancy_dictionary_list.sort(
                    key=lambda x: (datetime.strptime(x["published_at"], "%Y-%m-%dT%H:%M:%S%z")),
                    reverse=bool_sort_order)
                return vacancy_dictionary_list
            elif sortby == "Опыт работы":
                vacancy_dictionary_list.sort(
                    key=lambda x: self.experience_order[x["experience_id"]], reverse=bool_sort_order)
                return vacancy_dictionary_list
            else:
                vacancy_dictionary_list.sort(key=lambda x: x[self.rus_eng_conversion[sortby]], reverse=bool_sort_order)
                return vacancy_dictionary_list

        def filter_vacancies(filter_string, vacancy_dictionary_list):
            """Сортирует словарь вакансий по строке

            Args:
                filter_string (str): Строка содержащая параметр фильтрации и требуемую информацию

            Returns:
                list(dict)
            """
            if not filter_string:
                return vacancy_dictionary_list
            split_filter = filter_string.split(": ")
            ru_filter = split_filter[0]
            filter_parameter = split_filter[1]

            if ru_filter == "Дата публикации вакансии":
                formatted_vacancy_dictionary_list = []
                for dic in vacancy_dictionary_list:
                    raw_date = dic["published_at"]
                    date = raw_date.split("-")
                    date = f"{date[2][0:2]}.{date[1]}.{date[0]}"
                    if filter_parameter == date:
                        formatted_vacancy_dictionary_list.append(dic)
                result = formatted_vacancy_dictionary_list

            elif ru_filter == "Оклад":
                result = [c for c in vacancy_dictionary_list if
                          int(float(c["salary_from"])) <= int(filter_parameter) <= int(float(c["salary_to"]))]
            elif ru_filter == "Навыки":
                filter_parameter = filter_parameter.split(", ")
                result = [c for c in vacancy_dictionary_list if
                          all(x in c[self.rus_eng_conversion[ru_filter]] for x in filter_parameter)]
            elif ru_filter == "Идентификатор валюты оклада":
                result = [c for c in vacancy_dictionary_list if
                          self.currency_conversion_reversed[filter_parameter] == c["salary_currency"]]
            elif ru_filter == "Опыт работы":
                result = [c for c in vacancy_dictionary_list if
                          self.experience_conversion_reversed[filter_parameter] == c["experience_id"]]

            else:
                result = [c for c in vacancy_dictionary_list if
                          filter_parameter == c[self.rus_eng_conversion[ru_filter]]]

            if len(result) == 0:
                print("Ничего не найдено")
                exit()
            return result

        def formatter(row):
            """Форматирует ряд таблицы

            Args:
                row (dict): Словарь-ряд таблицы

            Returns:
                new_row (dict): Отформатированный словарь-ряд таблицы
            """
            new_row = row
            new_row["salary_currency"] = self.currency_conversion[row["salary_currency"]]
            new_row["experience_id"] = self.experience_conversion[row["experience_id"]]
            if new_row["premium"] == "True":
                new_row["premium"] = "Да"
            if new_row["premium"] == "False":
                new_row["premium"] = "Нет"
            date = new_row["published_at"]
            date = date.split("-")
            new_row["published_at"] = f"{date[2][0:2]}.{date[1]}.{date[0]}"
            salary_from = f'{int(float((new_row.pop("salary_from")))):,}'.replace(",", " ")
            salary_to = f'{int(float((new_row.pop("salary_to")))):,}'.replace(",", " ")
            salary_gross = new_row.pop("salary_gross")
            if (salary_gross == "TRUE" or salary_gross == "Да" or salary_gross == "true"):
                salary_gross = "(Без вычета налогов)"
            else:
                salary_gross = "(С вычетом налогов)"
            currency = new_row.pop("salary_currency")
            new_row["salary"] = f'{salary_from} - {salary_to} ({currency}) {salary_gross}'

            return new_row

        def print_vacancies(data_vacancies, dic_naming, vacancy_range, headers):
            """Печатает таблицу вакансий в консоль

            Args:
                data_vacancies (list(dict)): Список словарей вакансий
                dic_naming (list(str)): Заголовки таблицы
                vacancy_range (list(int)): Диапазон вывода вакансий
                headers (list(str)) : Требуемые столбцы таблицы
            """
            if len(data_vacancies) == 0:
                print("Нет данных")
                return
            table = PrettyTable(header=True, align="l", hrules=ALL)
            if len(vacancy_range) == 0:
                vacancy_range.append(1)
                vacancy_range.append(len(data_vacancies))
            elif len(vacancy_range) == 1:
                vacancy_range.append(len(data_vacancies))
            else:
                vacancy_range[1] -= 1

            header = [dic_naming[x] for x in dic_naming]
            for x in dic_naming:
                table.max_width[dic_naming[x]] = 20
            header.insert(0, "№")
            table.field_names = header
            for i in range(vacancy_range[0] - 1, vacancy_range[1]):
                formatted_dictionary = formatter(data_vacancies[i])
                row = [i + 1]
                for name in dic_naming:
                    formatted_name = formatted_dictionary[name]
                    if isinstance(formatted_dictionary[name], list):
                        formatted_name = "\n".join(formatted_dictionary[name])
                    if len(formatted_name) > 100:
                        formatted_name = formatted_name[0:100] + "..."
                    row.append(formatted_name)
                table.add_row(row)
            if not headers[0]:
                print(table)
            else:
                print(table.get_string(fields=["№"] + headers))

        vacancy_dictionary_list = dataset.vacancies_dicts
        if vacancy_dictionary_list == 0:
            print("Пустой файл")
            exit()

        print_vacancies(
            filter_vacancies
            (vacancy_contains, sorter(vacancies_sortby, vacanies_sort_order, vacancy_dictionary_list)),
            self.eng_rus_conversion, vacancy_range, headers)


file_name = input("Введите название файла: ")
vacancy_contains = input("Введите параметр фильтрации: ")
vacancies_sortby = input("Введите параметр сортировки: ")
vacanies_sort_order = input("Обратный порядок сортировки (Да / Нет): ")
vacancy_range = [int(x) for x in input("Введите диапазон вывода: ").split()]
headers = input("Введите требуемые столбцы: ").split(", ")
input_connect = InputConnect\
    (file_name, vacancy_contains, vacancies_sortby, vacanies_sort_order, vacancy_range, headers)
input_connect.parser_decorator(DataSet(file_name))
