from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class HhVacanciesLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()

    title_out = TakeFirst()
    salary_out = TakeFirst()
    description_out = TakeFirst()
    # key_skills_out = TakeFirst()
    employer_url_out = TakeFirst()


class HhEmployersLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()

    title_out = TakeFirst()
    website_out = TakeFirst()
    # activity_out = TakeFirst()
    description_out = TakeFirst()
    other_vacancies_out = TakeFirst()
