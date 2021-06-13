from urllib.parse import urljoin
from scrapy import Selector


def clear_data(data: str) -> str:
    return " ".join(data.split())


def organize_data(data: list) -> dict or str:
    if not data:
        return ''
    new_data = {}
    for index in range(len(data)):
        try:
            if index % 3 == 1:
                new_data[data[index][:-2]] = clear_data(data[index + 1])
        except IndexError as e:
            print('Под эти входящие данные этот шаблон не подходит! '
                  'Данные вернутся единым текстом вместо словаря')
            return clear_data(''.join(data))
    return new_data


def create_author_link(author_id: str) -> str:
    author = ""
    if author_id:
        author = urljoin("https://www.avito.ru/", author_id)
    return author
