import pymongo
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
            yield from self._get_follow(response, item["selector"], getattr(self, item["callback"]))

    def car_parse(self, response):
        data = {}
        for key, selector in CAR_DATA.items():
            try:
                data[key] = selector(response)
            except (ValueError, AttributeError):
                continue
        self.db_client[self.crawler.settings.get("BOT_NAME", "parser")][self.name].insert_one(data)
