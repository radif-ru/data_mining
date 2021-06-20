BRANDS = {
    "selector": "//div[contains(@class, 'Filters_brandsList')]"
                "//a[@data-target='brand']/@href",
    "callback": "brand_parse",
}
PAGINATION = {
    "selector": "//div[contains(@class, 'Paginator_block')]"
                "//a[@data-target-id='button-link-serp-paginator']/@href",
    "callback": "brand_parse",
}

CARS = {
    "selector": "//article[@data-target='serp-snippet']"
                "//a[@data-target='serp-snippet-title']/@href",
    "callback": "car_parse",
}

CAR_DATA = {
    "title": {"xpath": "//div[@data-target='advert-title']/text()"},
    "photos": {"xpath": "//img[contains(@class, 'PhotoGallery_photoImage')]/@src"},
    "characteristics": {"xpath": "//div[contains(@class, 'AdvertCard_specs')]"
                                 "/div/div[contains(@class, 'AdvertSpecs_row')]"},
    "price": {"xpath": "//div[@data-target='advert-price']/text()"},
    "descriptions": {"xpath": "//div[@data-target='advert-info-descriptionFull']/text()"},
    "author": {"xpath": '//script[contains(text(), "window.transitState = decodeURIComponent")]',
               "re": r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar"
               },
}
