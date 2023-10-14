"""
Svitochev K.
Notify about hot vacancies
"""
import requests
from datetime import datetime
from config import Config


def get_vacancy_details(data: dict) -> list:
    vacancy_details = []
    for item in data:
        salary = item.get('salary')
        if salary is not None and (salary.get('to') is not None and salary.get('to') < Config.HH_API_SALARY_TO):
            continue
        vacancy_details.append({'name': item.get('name'),
                                'salary': item.get('salary'),
                                'employer': item.get('employer'),
                                'alternate_url': item.get('alternate_url'),
                                'created_at': item.get('created_at'),
                                'published_at': item.get('published_at')}
                               )
    return vacancy_details


def get_vacancies_api(page=0, date_from=datetime.today().strftime("%Y-%m-%d")):
    params = {'text': Config.HH_API_TEXT,
              'area': 113,
              'page': page,
              'per_page': 100,
              # 'period': 4,
              'date_from': date_from,
              'schedule': Config.HH_API_SCHEDULE
              }
    request = requests.get(url=Config.HH_URL, params=params)

    if request.status_code == 200:
        return request.json()
    return None


def get_vacancies():
    data_json = get_vacancies_api(date_from=Config.HH_API_DATE_FROM)
    if data_json is None:
        return None
    pages = data_json.get('pages')
    vacancies = get_vacancy_details(data_json['items'])
    if pages > 1:
        for p in range(1, pages):
            data_json = get_vacancies_api(page=p, date_from=Config.HH_API_DATE_FROM)
            vacancies += get_vacancy_details(data_json['items'])

    return vacancies


def serializer(vacancy):
    # data = f"<b>{vacancy.get('name')}</b>\n"
    # salary = vacancy.get('salary')
    # if salary is not None:
    #     data += f"З/п от {salary.get('from')} до {salary.get('to')}\n"
    # data += (f"Фирма: {vacancy.get('employer').get('name')}\n"
    #          f"Создана: {vacancy.get('created_at').replace('T', ' ')[:-8]}\n"
    #          f"Опублик: {vacancy.get('published_at').replace('T', ' ')[:-8]}\n"
    #          f"Ссылка: {vacancy.get('alternate_url')}"
    #          )
    data = (f"Ссылка: {vacancy.get('alternate_url')}\n"
            f"Созд.: {vacancy.get('created_at').replace('T', ' ')[:-8]}\n"
            f"Опуб.: {vacancy.get('published_at').replace('T', ' ')[:-8]}\n"
            )
    return data


def send_to_telegram(message):
    url = Config.TG_URL + f'chat_id={Config.TG_ID}&parse_mode=HTML&text={message}'
    response = requests.get(url)
    print(response.status_code)


def main():
    vacancy = get_vacancies()
    for item in vacancy:
        message = serializer(item)
        send_to_telegram(message)


if __name__ == '__main__':
    main()
