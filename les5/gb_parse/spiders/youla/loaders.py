from scrapy.loader import ItemLoader

from .processors import clear_price, get_characteristics, create_author_link
from itemloaders.processors import TakeFirst, MapCompose


class AutoyoulaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    descriptions_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics)
    author_in = MapCompose(create_author_link)
    author_out = TakeFirst()
