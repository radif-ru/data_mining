from scrapy import Selector


def clean_parameters(item):
    selector = Selector(text=item)
    data = {
        "name": selector.xpath("//span[@class='item-params-label']/text()").extract_first(),
        "value": selector.xpath("//a[contains(@class, 'item-params-link')]/text()").get(),
    }
    if not data["value"]:
        value_result = ""
        for item in selector.xpath("//li/text()").extract():
            if item and not item.isspace():
                value_result += item
        data["value"] = value_result
    return data


def to_type(type_cls):
    def procedure(item):
        try:
            data = type_cls(item)
        except ValueError:
            data = None
        return data

    return procedure
