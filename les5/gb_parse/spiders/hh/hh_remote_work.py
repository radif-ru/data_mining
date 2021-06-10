import scrapy
import pymongo

from .loaders import HhVacanciesLoader, HhEmployersLoader


class HhRemoteWorkSpider(scrapy.Spider):
    name = 'hh_remote_work'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def parse(self, response: scrapy.Request, **kwargs):
        next_page = response.xpath(
            '//div[@data-qa="pager-block"]//a[@data-qa="pager-next"]/@href') \
            .extract_first()
        next_page = response.urljoin(next_page)
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.xpath(
            '//div[contains(@class, "vacancy-serp-item")]'
            '//a[@class="bloko-link" '
            'and @data-qa="vacancy-serp__vacancy-title"]/@href').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: scrapy.Request):
        loader = HhVacanciesLoader(response=response)
        title = response.xpath(
            '//div[@class="vacancy-title"]//h1/text()').extract_first()
        loader.add_value("title", title)
        salary = ''.join(response.xpath(
            '//p[@class="vacancy-salary"]/span/text()').extract())
        loader.add_value('salary', salary)
        required_experience = ''.join(response.xpath(
            '//div[@class="vacancy-description"]/div[1]/div[1]/p[1]//text()'
        ).extract())
        employment = ''.join(response.xpath(
            '//div[@class="vacancy-description"]/div[1]/div[1]/p[2]//text()'
        ).extract())
        detailed = ''.join(response.xpath(
            '//div[@itemprop="description"]//text()').extract())

        description = {
            'required_experience': required_experience,
            'employment': employment,
            'detailed': detailed
        }
        loader.add_value('description', description)

        key_skills = response.xpath(
            '//div[@class="bloko-tag-list"]'
            '//div[contains(@data-qa, "skills-element")]//text()').extract()
        loader.add_value('key_skills', key_skills)

        employer_url = response.urljoin(response.xpath(
            '//a[@class="vacancy-company-name"]/@href').extract_first())
        loader.add_value('employer_url', employer_url)

        yield loader.load_item()
        yield response.follow(employer_url, callback=self.employer_parse)

    def employer_parse(self, response: scrapy.Request):
        loader = HhEmployersLoader(response=response)
        title = response.xpath(
            '//span[@class="company-header-title-name"]//text()'
        ).extract_first() or ''.join(response.xpath(
            '//div[@class="tmpl_hh_home_intro__title"]//text()').extract()) \
                    .replace('\u202f', ' ').replace('\n', '').replace('  ', '')
        loader.add_value('title', title)
        website = response.xpath(
            '//a[@data-qa="sidebar-company-site"]/@href').extract_first() \
                  or response.xpath(
            '//div[@class="tmpl_hh_home_intro"]/a/@href').extract_first()
        loader.add_value('website', website)
        activity = response.xpath(
            '//div[@class="tmpl_hh_red"]'
            '//div[@class="tmpl_hh_red__item"]//p/text()').extract()
        loader.add_value('activity', activity)
        description = response.xpath(
            '//div[@class="company-description"]//p/text()').extract()
        loader.add_value('description', description)

        other_vacancies = response.urljoin(response.xpath(
            '//a[@data-qa="employer-page__employer-vacancies-link"]/@href'
        ).extract_first())
        loader.add_value('other_vacancies', other_vacancies)

        yield loader.load_item()
        yield response.follow(other_vacancies, callback=self.parse)
