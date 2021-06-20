from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class TagLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    date_parse_out = TakeFirst()
    data_out = TakeFirst()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "tag")


class ItemTagLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    date_parse_out = TakeFirst()
    data_out = TakeFirst()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "item_tag")
