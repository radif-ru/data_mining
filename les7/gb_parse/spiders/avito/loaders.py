from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

from .processors import clean_parameters, to_type
from .xpath_selectors import ADS_DATA


class AvitoRealEstateLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = TakeFirst()
    price_in = MapCompose(to_type(float))
    address_out = TakeFirst()
    parameters_in = MapCompose(clean_parameters)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "real_estate")
        for key, selector in ADS_DATA.items():
            self.add_xpath(key, **selector)
