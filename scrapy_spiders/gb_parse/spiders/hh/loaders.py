from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from .processors import flat_text, hh_user_url, hh_sphere_activities_clean, concatenate_items


class HHVacancyLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    description_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "vacancy")


class HHCompanyLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()
    company_name_in = concatenate_items
    company_name_out = TakeFirst()
    company_site_out = TakeFirst()
    sphere_activities_in = MapCompose(hh_sphere_activities_clean)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "company")
