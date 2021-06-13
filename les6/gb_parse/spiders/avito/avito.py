import pymongo
import scrapy

from .xpath_selectors import APARTMENTS, PAGINATION, APARTMENT_DATA
from .loaders import AvitoLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru', '*.avito.ru']

    def __init__(self, mark, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()
        self.start_urls = [f'https://www.avito.ru/{mark}/kvartiry/prodam']

    def _get_follow(self, response, xpath, callback):
        for a_link in response.xpath(xpath):
            yield response.follow(a_link, callback=callback)

    def parse(self, response):
        for item in (PAGINATION, APARTMENTS):
            yield from self._get_follow(
                response,
                item["selector"],
                getattr(self, item["callback"])
            )

    def apartment_parse(self, response):
        loader = AvitoLoader(response=response)
        for key, value in APARTMENT_DATA.items():
            loader.add_xpath(field_name=key, **value)
        yield loader.load_item()
