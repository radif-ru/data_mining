import pymongo
import scrapy
from .xpath_selectors import BRANDS, PAGINATION, CARS, CAR_DATA
from .loaders import AutoyoulaLoader


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.xpath(selector_str):
            yield response.follow(a_link, callback=callback)

    def parse(self, response):
        yield from self._get_follow(
            response,
            BRANDS["selector"],
            getattr(self, BRANDS["callback"])
        )

    def brand_parse(self, response):
        for item in (PAGINATION, CARS):
            yield from self._get_follow(response, item["selector"], getattr(self, item["callback"]))

    def car_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        loader.add_value("url", response.url)
        for key, value in CAR_DATA.items():
            loader.add_xpath(field_name=key, **value)
        yield loader.load_item()
