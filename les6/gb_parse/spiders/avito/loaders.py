from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

from les6.gb_parse.spiders.avito.processors import organize_data, \
    create_author_link, clear_data


class AvitoLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = TakeFirst()
    address_in = MapCompose(clear_data)
    address_out = TakeFirst()
    parameters_in = organize_data
    parameters_out = TakeFirst()
    author_link_in = MapCompose(create_author_link)
    author_link_out = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "apartments")
