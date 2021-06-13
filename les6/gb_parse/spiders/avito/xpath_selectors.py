PAGINATION = {
    'selector': '//div[contains(@class, "pagination-pages")]'
                '//a[@class="pagination-page"]/@href',
    'callback': "parse",
}

APARTMENTS = {
    'selector': '//div[@data-marker="catalog-serp"]//div[@data-marker="item"]'
                '//a[@data-marker="item-title"]/@href',
    'callback': "apartment_parse",
}

APARTMENT_DATA = {
    'title': {'xpath': '//h1[@class="title-info-title"]'
                       '/span[@class="title-info-title-text"]/text()'},
    'price': {'xpath': '//div[@class="item-price"]//span[@itemprop="price"]'
                       '/@content'},
    'address': {'xpath': '//div[@class="item-address"]'
                         '//span[contains(@class, "item-address__string")][1]'
                         '/text()'},
    'parameters': {'xpath': '//div[@class="item-params"]'
                            '//li[@class="item-params-list-item"]//text()'},
    'author_link': {'xpath': '//div[@class="seller-info-value"]//a/@href'},
    'photos': {'xpath': '//div[contains(@class, "gallery-img-frame")]'
                        '/@data-url'}

}
