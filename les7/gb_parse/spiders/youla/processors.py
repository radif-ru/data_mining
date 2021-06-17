from urllib.parse import urljoin
from scrapy import Selector


def clear_price(price: str) -> float:
    try:
        result = float(price.replace("\u2009", ""))
    except ValueError:
        result = None
    return result


def get_characteristics(item: str):
    selector = Selector(text=item)
    data = {
        "name": selector.xpath("//div[contains(@class, 'AdvertSpecs_label')]/text()").get(),
        "value": selector.xpath("//div[contains(@class, 'AdvertSpecs_data')]//text()").get(),
    }
    return data


def create_author_link(author_id: str) -> str:
    author = ""
    if author_id:
        author = urljoin("https://youla.ru/user/", author_id)
    return author
