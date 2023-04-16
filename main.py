import requests


def fetch_vacancy(search_field) -> list:
    page, vacancies = 0, []
    url = "https://api.hh.ru/vacancies"
    payload = {
        "text": f"NAME:Программист AND {search_field}",
        "area": 1,
        "only_with_salary": True,
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


def predict_rub_salary(vacancy: dict) -> float|None:
    about_salary = vacancy.get("salary")
    if about_salary.get("currency") != "RUR":
        return None
    if about_salary.get("from") is None:
        return about_salary.get("to") * 0.8
    return about_salary.get("from") * 1.2


def about_vacancies(vacancies: list) -> list:
    salaries = [predict_rub_salary(vacancy) for vacancy in vacancies
                if predict_rub_salary(vacancy) is not None]
    vacancies_processed = len(salaries)
    average_salery = int(sum(salaries) / vacancies_processed)
    return [len(vacancies), vacancies_processed, average_salery]


def main():
    languages = [
        "TypeScript", "Swift", "Scala", "Objective-C", "Shell", "Go",
        "C++", "C#", "PHP" , "Ruby", "Python", "Java", "JavaScript"
        ]
    keys = ["vacancies_found", "vacancies_processed","average_salary"]
    jobs = {}
    for language in languages:
        about_vacancies(fetch_vacancy(language))
        language_vacancies = dict(zip(keys, about_vacancies(fetch_vacancy(language))))
        jobs[language] = language_vacancies
    print(jobs)


if __name__ == "__main__":
    main()
