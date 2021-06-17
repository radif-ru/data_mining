import json
from datetime import datetime

import scrapy
from les7.gb_parse.spiders.instagram.loaders import TagLoader, ItemTagLoader


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com', 'instagram.com']
    start_urls = ['https://www.instagram.com/accounts/login/']
    _login_path = "/accounts/login/ajax/"
    _tags_path = "/explore/tags/{tag}/"

    def __init__(self, login, password, tags, *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                response.urljoin(self._login_path),
                method="POST",
                callback=self.parse,
                formdata={
                    "username": self.login,
                    "enc_password": self.password,
                },
                headers={
                    "X-CSRFToken": js_data["config"]["csrf_token"],
                }
            )
        except AttributeError:
            r_data = response.json()
            if r_data.get("authenticated"):
                for tag in self.tags:
                    url = self._tags_path.format(tag=tag)
                    yield response.follow(
                        url, callback=self.tag_page_parse, headers={
                            'surface': 'list'
                        })

    def tag_page_parse(self, response):
        tag_loader = TagLoader(response=response)
        js_data = self.js_data_extract(response)

        date_parse = datetime.now().isoformat()
        data = js_data['entry_data']['TagPage'][0]['data']
        tag_loader.add_value('date_parse', date_parse)
        tag_loader.add_value('data', data)
        yield tag_loader.load_item()

        for items in data['recent']['sections']:
            for el in items['layout_content']['medias']:
                item_loader = ItemTagLoader(response=response)
                date_parse = datetime.now().isoformat()
                data = el['media']
                photos = [img['url'] for img in
                          el['media']['image_versions2']['candidates']]
                item_loader.add_value('date_parse', date_parse)
                item_loader.add_value('data', data)
                item_loader.add_value('photos', photos)
                yield item_loader.load_item()

    def js_data_extract(self, response):
        js = response.xpath(
            "//script[contains(text(), 'window._sharedData = ')]/text()").extract_first()
        start_idx = js.index("{")
        data = json.loads(js[start_idx:-1])
        return data
