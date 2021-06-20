from copy import copy
from urllib.parse import urlencode

import scrapy

from .loaders import HHVacancyLoader, HHCompanyLoader
from .xpath_selectors import PAGINATION, VACANCY, VACANCY_DATA, COMPANY_DATA


class HhRemoteSpider(scrapy.Spider):
    name = "hh_remote"
    allowed_domains = ["hh.ru", "*.hh.ru"]
    start_urls = [
        "https://krasnodar.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113"
    ]
    api_vacancy_list_path = "/shards/employerview/vacancies"
    api_vacancy_list_params = {
        "page": 0,
        "currentEmployerId": None,
        "json": True,
        "regionType": "OTHER",
        "disableBrowserCache": True,
    }

    def _get_follow(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        for item in (PAGINATION, VACANCY):
            yield from self._get_follow(response, item["selector"], getattr(self, item["callback"]))

    def vacancy_parse(self, response):
        loader = HHVacancyLoader(response=response)
        for key, xpath in VACANCY_DATA.items():
            loader.add_xpath(key, **xpath)
        data = loader.load_item()
        yield response.follow(data['author'], callback=self.company_parse)
        yield data

    def company_parse(self, response):
        loader = HHCompanyLoader(response=response)
        for key, xpath in COMPANY_DATA.items():
            loader.add_xpath(key, **xpath)
        data = loader.load_item()
        employer_id = response.url.split("/")[-1]
        params = copy(self.api_vacancy_list_params)
        params["currentEmployerId"] = employer_id
        yield response.follow(
            self.api_vacancy_list_path + "?" + urlencode(params),
            callback=self.api_vacancy_list_parse,
            cb_kwargs=params
        )
        yield data

    def api_vacancy_list_parse(self, response, **params):
        data = response.json()
        if data['@hasNextPage']:
            params["page"] += 1
            yield response.follow(
                self.api_vacancy_list_path + "?" + urlencode(params),
                callback=self.api_vacancy_list_parse,
                cb_kwargs=params
            )
        for vacancy in data['vacancies']:
            yield response.follow(
                vacancy["links"]["desktop"],
                callback=self.vacancy_parse
            )
