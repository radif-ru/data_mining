import scrapy
import pymongo

from .loaders import HhVacanciesLoader, HhEmployersLoader
from .processors import clear_employer_title
from .xpath_selectors import PAGINATION, VACANCY, EMPLOYER


class HhRemoteWorkSpider(scrapy.Spider):
    name = 'hh_remote_work'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def parse(self, response: scrapy.Request, **kwargs):
        next_page = response.xpath(PAGINATION['next']).extract_first()
        next_page = response.urljoin(next_page)
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath(VACANCY['urls_list']).extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: scrapy.Request):
        loader = HhVacanciesLoader(response=response)
        loader.add_value('item_type', 'vacancy')
        loader.add_value('url', response.url)

        title = response.xpath(VACANCY['title']).extract_first()
        loader.add_value("title", title)

        salary = ''.join(response.xpath(VACANCY['salary']).extract())
        loader.add_value('salary', salary)

        required_experience = ''.join(
            response.xpath(VACANCY['description']['required_experience']
                           ).extract())
        employment = ''.join(
            response.xpath(VACANCY['description']['employment']
                           ).extract())
        detailed = ''.join(
            response.xpath(VACANCY['description']['detailed']
                           ).extract())
        description = {
            'required_experience': required_experience,
            'employment': employment,
            'detailed': detailed
        }
        loader.add_value('description', description)

        key_skills = response.xpath(VACANCY['key_skills']).extract()
        loader.add_value('key_skills', key_skills)

        employer_url = response.urljoin(
            response.xpath(VACANCY['employer_url']).extract_first())
        loader.add_value('employer_url', employer_url)

        yield loader.load_item()
        yield response.follow(employer_url, callback=self.employer_parse)

    def employer_parse(self, response: scrapy.Request):
        loader = HhEmployersLoader(response=response)
        loader.add_value('item_type', 'employer')
        loader.add_value('url', response.url)

        title = clear_employer_title(
            response.xpath(EMPLOYER['title_vars'][0]).extract()) \
                or clear_employer_title(
            response.xpath(EMPLOYER['title_vars'][1]).extract())
        loader.add_value('title', title)

        website = response.xpath(EMPLOYER['website_vars'][0]).extract_first() \
                  or response.xpath(
            EMPLOYER['website_vars'][1]).extract_first()
        loader.add_value('website', website)

        activity = response.xpath(EMPLOYER['activity']).extract()
        loader.add_value('activity', activity)

        description = response.xpath(EMPLOYER['description']).extract()
        loader.add_value('description', description)

        other_vacancies = response.urljoin(
            response.xpath(EMPLOYER['other_vacancies']).extract_first())
        loader.add_value('other_vacancies', other_vacancies)

        yield loader.load_item()
        if other_vacancies:
            yield response.follow(other_vacancies, callback=self.parse)
