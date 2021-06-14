import base64
import os
from urllib.parse import urljoin

import requests
from les6.gb_parse.settings import PHONE_NUMBERS
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


def get_phone_num(response):
    apartment_id = response.url.split('_')[-1]
    phone_url_data = f'https://www.avito.ru/web/1/items/phone/' \
                     f'{apartment_id}'
    resp = requests.get(phone_url_data)
    if resp:
        resp_data = resp.json()
        bs64_img = resp_data['image64'].split(',')[1]
        bs64_bytes = bs64_img.encode('utf-8')
        if not os.path.isdir(PHONE_NUMBERS):
            os.mkdir(PHONE_NUMBERS)
        img_name = os.path.join(PHONE_NUMBERS, f'{apartment_id}.png')
        with open(img_name, 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(bs64_bytes)
            file_to_save.write(decoded_image_data)
        return img_name
    return ''
