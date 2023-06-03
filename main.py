import os
import requests
from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable


def fetch_hh_vacancies(search_field: str) -> list:
    '''Finds jobs from hh.ru by the specified search field and
       displays list of jobs'''

    page, vacancies, url = 0, [], "https://api.hh.ru/vacancies"
    moscow_area_code, vacancies_per_page = 1, 100
    payload = {
        "text": f"NAME:Программист AND {search_field}",
        "area": moscow_area_code,
        "per_page": vacancies_per_page,
        "page": page
    }
    pages_number = 1
    while page <= pages_number:
        vacancy_response = requests.get(url, params=payload)
        vacancy_response.raise_for_status()

        vacancy_payload = vacancy_response.json()
        pages_number = vacancy_payload.get('pages')
        vacancies.extend(vacancy_payload.get('items'))
        page += 1
    return vacancies


def fetch_sj_vacancies(search_field: str, token: str) -> list:
    '''Finds jobs from superjob.ru by the specified search field and
       displays list of jobs'''
    headers = {
        "X-Api-App-Id": token,
        "Authorization": "Bearer r.000000010000001.example.access_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    pages_number, page, vacancies = 1, 0, []
    specialization_code, vacancies_per_page = 48, 100
    url = "https://api.superjob.ru/2.0/vacancies/"
    payload = {
        "town": "Москва",
        "catalogues": specialization_code,
        "keyword": search_field,
        "count": vacancies_per_page,
        "page": page
    }
    while page < pages_number:
        vacancy_response = requests.get(url, headers=headers, params=payload)
        vacancy_response.raise_for_status()

        vacancy_payload = vacancy_response.json()
        pages_number = round(vacancy_payload.get('total') / vacancies_per_page)
        vacancies.extend(vacancy_payload.get('objects'))
        page += 1
    return vacancies


def get_hh_salary_from_and_to(vacancy: dict) -> tuple[float] | tuple[None]:
    '''Gets 'salary from' and 'salary to' for vacancy on hh.ru'''
    salary = vacancy.get("salary")
    if not salary or salary.get("currency") != "RUR":
        return None, None
    salary_from = salary.get("from")
    salary_to = salary.get("to")
    if not salary_from:
        salary_from = None
    if not salary_to:
        salary_to = None
    return salary_from, salary_to


def get_sj_salary_from_and_to(vacancy: dict) -> tuple[float] | tuple[None]:
    '''Gets "salary from" and "salary to" for vacancy on superjob.ru'''
    salary_from = vacancy.get("payment_from")
    salary_to = vacancy.get("payment_to")
    if not salary_from:
        salary_from = None
    if not salary_to:
        salary_to = None
    return salary_from, salary_to


def predict_salary(salary_from: float, salary_to: float) -> None | float:
    '''Predicts salary of vacancy with use of "salary_from" and "salary_to"'''
    if not salary_from and not salary_to:
        return None
    if not salary_from:
        return int(salary_to * 0.8)
    if not salary_to:
        return int(salary_from * 1.2)
    average_salary = (salary_from + salary_to) / 2
    return round(average_salary)


def get_vacancy_statistics(vacancies: list,
                           get_salary: callable) -> tuple | None:
    '''Creates tuple with count of all found vacancies, processed vacancies
    and calculated average salary of all jobs'''
    salaries = [
        salary for salary in (
            predict_salary(*get_salary(vacancy=vacancy))
            for vacancy in vacancies)
        if salary
    ]
    vacancies_found = len(vacancies)
    if salaries:
        vacancies_processed = len(salaries)
        average_salary = int(sum(salaries) / vacancies_processed)
        return vacancies_found, vacancies_processed, average_salary
    return vacancies_found, 0, 0


def parse_hh_vacancies(search_keywords: tuple) -> dict:
    '''Parses jobs by search_keywords from hh.ru and returns information
       for each of them with the addition of columns:
        "vacancies_found", "vacancies_processed", "average_salary"
    '''
    vacancy_statistics_by_search_keywords = {}
    keys = ("vacancies_found", "vacancies_processed", "average_salary")
    for search_keyword in search_keywords:
        all_vacancies = fetch_hh_vacancies(search_keyword)
        if not all_vacancies:
            vacancy_statistics_by_search_keywords[search_keyword] = 0
            continue
        vacancy_statistics = get_vacancy_statistics(
            vacancies=all_vacancies, get_salary=get_hh_salary_from_and_to)
        vacancy_statistics_by_search_keywords[search_keyword] = {
            key: vacancy_statistics[ind] for ind, key in enumerate(keys)}
    return vacancy_statistics_by_search_keywords


def parse_sj_vacancies(search_keywords: tuple, token: str) -> dict:
    '''Parses jobs by search_keywords from superjob.ru and returns information
       for each of them with the addition of columns:
       "vacancies_found", "vacancies_processed", "average_salary"
    '''
    vacancy_statistics_by_search_keywords = {}
    keys = ("vacancies_found", "vacancies_processed", "average_salary")
    for search_keyword in search_keywords:
        all_vacancies = fetch_sj_vacancies(search_keyword, token=token)
        if not all_vacancies:
            vacancy_statistics_by_search_keywords[search_keyword] = dict(
                zip(keys, (0, 0, 0)))
            continue
        vacancy_statistics = get_vacancy_statistics(
            vacancies=all_vacancies, get_salary=get_sj_salary_from_and_to)
        vacancy_statistics_by_search_keywords[search_keyword] = {
            key: vacancy_statistics[ind] for ind, key in enumerate(keys)}
    return vacancy_statistics_by_search_keywords


def create_table(jobs: dict, title=None) -> AsciiTable:
    '''Creates table to display the data in a readable form'''
    column_names = ["Язык программирования", "Вакансий найдено",
                    "Вакансий обработано", "Средняя зарплата"]

    def get_table_data(jobs: dict) -> list:
        '''Creates list of data to be displayed in table'''
        table_data = [[language_name, *job_stats.values()]
                      if job_stats else [language_name, job_stats]
                      for language_name, job_stats in jobs.items()]
        return table_data

    def make_table(table_data: list) -> AsciiTable:
        '''Creates the table using the provided data'''
        jobs_table = AsciiTable([column_names, *table_data], title=title)
        return jobs_table.table

    return make_table(table_data=get_table_data(jobs=jobs))


def main():
    load_dotenv(find_dotenv())
    sj_token = os.environ["TOKEN_SUPERJOB"]
    languages = ("TypeScript", "Swift", "Scala", "Objective-C", "Shell", "Go",
                 "C++", "C#", "PHP", "Ruby", "Python", "Java", "JavaScript")
    hh_table = create_table(parse_hh_vacancies(languages),
                            title='HeadHunter Moscow')
    sj_table = create_table(parse_sj_vacancies(languages, token=sj_token),
                            title='SuperJob Moscow')
    print(hh_table, sj_table, sep='\n\n')


if __name__ == "__main__":
    main()
