import os
import requests
from dotenv import load_dotenv, find_dotenv


def fetch_hh_vacancy(search_field: str) -> list:
    '''Finds jobs from hh.ru by the specified search field and
       displays list of jobs'''

    page, vacancies, url = 0, [], "https://api.hh.ru/vacancies"
    payload = {
        "text": f"NAME:Программист AND {search_field}",
        "area": 1,
        "per_page": 100,
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


def fetch_sj_vacancy(search_field: str) -> list:
    '''Finds jobs from superjob.ru by the specified search field and
       displays list of jobs'''
    load_dotenv(find_dotenv())
    headers = {
        "X-Api-App-Id": os.environ["TOKEN_SUPERJOB"],
        "Authorization": "Bearer r.000000010000001.example.access_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    pages_number, page, vacancies = 1, 0, []
    url = "https://api.superjob.ru/2.0/vacancies/"
    payload = {
        "town": "Москва",
        "catalogues": 48,
        "keyword": search_field,
        "count": 100,
        "page": page
    }
    while page < pages_number:
        vacancy_response = requests.get(url, headers=headers, params=payload)
        vacancy_response.raise_for_status()

        vacancy_payload = vacancy_response.json()
        pages_number = round(vacancy_payload.get('total') / 100)
        vacancies.extend(vacancy_payload.get('objects'))
        page += 1
    return vacancies


def predict_rub_salary_hh(vacancy: dict) -> tuple[float] | tuple[None]:
    '''Gets 'salary from' and 'salary to' for vacancy on hh.ru'''
    salary = vacancy.get("salary")
    if salary is None or salary.get("currency") != "RUR":
        return None, None
    salary_from = salary.get("from")
    salary_to = salary.get("to")
    return salary_from, salary_to


def predict_rub_salary_sj(vacancy: dict) -> None | float:
    '''Gets 'salary from' and 'salary to' for vacancy on superjob.ru'''
    salary_from = vacancy.get("payment_from")
    salary_to = vacancy.get("payment_to")
    return salary_from, salary_to


def predict_salary(salary_from: float, salary_to: float) -> None | float:
    '''Predicts salary of vacancy with use of "salary_from" and "salary_to"'''
    if ((salary_from is None or not salary_from)
            and (salary_to is None or not salary_to)):
        return None
    if salary_from is None or not salary_from:
        return int(salary_to * 0.8)
    if salary_to is None or not salary_to:
        return int(salary_from * 1.2)
    return round((salary_from + salary_to) / 2)


def about_vacancies(vacancies: list, predict_rub_salary) -> tuple | None:
    '''Creates tuple with count of all found vacancies, processed vacancies
    and calculated average salary of all jobs'''
    salaries = [el for el in (
                    predict_salary(*predict_rub_salary(vacancy=vacancy))
                    for vacancy in vacancies)
                if el not in (None, 0)]
    vacancies_found = len(vacancies)
    if not salaries:
        return vacancies_found, 0, 0
    vacancies_processed = len(salaries)
    average_salery = int(sum(salaries) / vacancies_processed)
    return len(vacancies), vacancies_processed, average_salery


def parse_hh_vacancies(search_keywords: tuple) -> dict:
    '''Parses jobs by search_keywords from hh.ru and returns information
       for each of them with the addition of columns:
        "vacancies_found", "vacancies_processed", "average_salary"
    '''
    jobs = {}
    keys = ("vacancies_found", "vacancies_processed", "average_salary")
    for keyword in search_keywords:
        all_vacancies = fetch_hh_vacancy(keyword)
        if not all_vacancies:
            jobs[keyword] = 0
            continue
        vacancy_data = about_vacancies(
            vacancies=all_vacancies, predict_rub_salary=predict_rub_salary_hh)
        jobs[keyword] = dict(zip(keys, vacancy_data))
    return jobs


def parse_sj_vacancies(search_keywords: tuple) -> dict:
    '''Parses jobs by search_keywords from superjob.ru and returns information
       for each of them with the addition of columns:
       "vacancies_found", "vacancies_processed", "average_salary"
    '''
    jobs = {}
    keys = ("vacancies_found", "vacancies_processed", "average_salary")
    for keyword in search_keywords:
        all_vacancies = fetch_sj_vacancy(keyword)
        if not all_vacancies:
            jobs[keyword] = 0
            continue
        vacancy_data = about_vacancies(
            vacancies=all_vacancies, predict_rub_salary=predict_rub_salary_sj)
        jobs[keyword] = dict(zip(keys, vacancy_data))
    return jobs


def main():
    languages = ("TypeScript", "Swift", "Scala", "Objective-C", "Shell", "Go",
                 "C++", "C#", "PHP", "Ruby", "Python", "Java", "JavaScript")
    print(parse_sj_vacancies(languages), parse_hh_vacancies(languages),
          sep='\n\n')


if __name__ == "__main__":
    main()
