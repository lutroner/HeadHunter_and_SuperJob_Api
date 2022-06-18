import requests
from pprint import pprint
import environs

HH_BASE_URL = 'https://api.hh.ru/vacancies'
PROGRAMMING_CATEGORY_ID = 96
SEARCH_PERIOD = 30
AREA_ID = 1
PROGRAMMING_LANGUAGES = ('Python', 'Java', 'Perl', 'JavaScript', 'C++', 'C#', 'Go', 'Ruby', 'Php', 'Rust')


def predict_rub_salary(vacancy):
    if vacancy['from'] and vacancy['to']:
        return (vacancy['from'] + vacancy['to']) / 2
    elif vacancy['from'] and vacancy['to'] is None:
        return vacancy['from'] * 1.2
    elif vacancy['from'] is None and vacancy['to']:
        return vacancy['to'] * 0.8
    else:
        return None


def get_headhunter_vacancies():
    vacancies = {}
    for language in PROGRAMMING_LANGUAGES:
        payload = {'professional_role': PROGRAMMING_CATEGORY_ID,
                   'period': SEARCH_PERIOD,
                   'area': AREA_ID,
                   'text': language
                   }
        response = requests.get(HH_BASE_URL, params=payload)
        response.raise_for_status()
        vacancies[language] = response.json()['found']
    return vacancies


def get_python_salary():
    payload = {'professional_role': PROGRAMMING_CATEGORY_ID,
               'period': SEARCH_PERIOD,
               'area': AREA_ID,
               'text': 'python'
               }
    response = requests.get(HH_BASE_URL, params=payload)
    response.raise_for_status()
    for vacancy in response.json()['items']:
        try:
            print(predict_rub_salary(vacancy['salary']), vacancy['salary'])
        except TypeError as e:
            print(None)


def main():
    # pprint(get_headhunter_vacancies())
    get_python_salary()


if __name__ == '__main__':
    main()
