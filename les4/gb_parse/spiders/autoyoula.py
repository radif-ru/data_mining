from base64 import b64decode
from urllib.parse import urljoin

import pymongo
import requests
import scrapy

from .css_selectors import BRANDS, CARS, PAGINATION, CAR_DATA


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.css(selector_str):
            url = a_link.attrib.get("href")
            yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self._get_follow(
            response,
            BRANDS["selector"],
            getattr(self, BRANDS["callback"])
        )

    def brand_parse(self, response):
        for item in (PAGINATION, CARS):
            yield from self._get_follow(response, item["selector"],
                                        getattr(self, item["callback"]))

    def car_parse(self, response):
        data = {}
        for key, selector in CAR_DATA.items():
            try:
                data[key] = selector(response)
            except (ValueError, AttributeError):
                continue
        data['phone_number'] = get_author_number(response) or 0
        self.db_client[self.crawler.settings.get("BOT_NAME", "parser")][
            self.name].insert_one(data)


def get_author_number(resp: scrapy.Request) -> str:
    post_url = resp.url
    post_id = post_url[post_url.find('--') + 2:]
    data_url = urljoin(
        'https://auto.youla.ru/api/get-similar-adverts/',
        f'?advertId={post_id}')
    response = requests.get(data_url)
    if response.status_code == 200:
        phone_number = response.json()[0]['phone']
        return b64decode(b64decode(phone_number)).decode()
