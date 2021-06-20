import json
import datetime

import requests
import scrapy
from les7.gb_parse.spiders.instagram.loaders import TagLoader, ItemTagLoader


def get_date_time():
    offset = datetime.timezone(datetime.timedelta(hours=3))
    date_time = datetime.datetime.now(offset)
    return date_time


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
                        })

    def tag_page_parse(self, response):
        try:
            tag_loader = TagLoader(response=response)
            js_data = self.js_data_extract(response)

            date_parse = get_date_time()
            data = js_data['entry_data']['TagPage'][0]['data']
            tag_loader.add_value('date_parse', date_parse)
            tag_loader.add_value('data', data)
            yield tag_loader.load_item()

            for items in data['recent']['sections']:
                for el in items['layout_content']['medias']:
                    item_loader = ItemTagLoader(response=response)
                    date_parse = get_date_time()
                    data = el['media']
                    item_loader.add_value('date_parse', date_parse)
                    item_loader.add_value('data', data)
                    if 'image_versions2' in el['media']:
                        photos = [img['url'] for img in
                                  el['media']['image_versions2']['candidates']]
                        item_loader.add_value('photos', photos)
                    yield item_loader.load_item()

            next_max_id = js_data['entry_data']['TagPage'][0]['data'][
                'recent']['next_max_id']
            next_page = js_data['entry_data']['TagPage'][0]['data'][
                'recent']['next_page']

            url = f'https://i.instagram.com/api/v1/tags/' \
                  f'{response.url.split("/")[-2]}/sections/'
            params = {
                'include_persistent': '0',
                'max_id': next_max_id,
                'page': str(next_page),
                # 'surface': 'list',
                'surface': 'grid',
                'tab': 'recent'
            }
            headers = {
                # 'Accept': '/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3,',
                'Alt-Used': 'i.instagram.com',
                'Connection': 'keep-alive',
                'Content-Length': '183',
                'Content-Type': 'application/x-www-form-urlencoded',
                # 'Cookie': '',
                # 'Host': 'i.instagram.com',
                # 'Origin': 'https://www.instagram.com',
                # 'Referer': 'https://www.instagram.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'X-ASBD-ID': '437806',
                "X-CSRFToken": js_data["config"]["csrf_token"],
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': 'hmac.AR0Ad5XkphMCEziLNkG0lNqAP2Bbw7DDghc0V8htgpo_-fe1',
                'X-Instagram-AJAX': js_data['rollout_hash'],
            }
            response_next_page = requests.post(
                url=url,
                data=params,
                headers=headers
            )

            # # yield scrapy.FormRequest(
            # response_next_page_scrapy = scrapy.FormRequest(
            #     url,
            #     # response.urljoin(f'/api/v1/tags/{response.url.split("/")[-2]}/sections/'),
            #     # callback=self.tag_page_parse,
            #     method="POST",
            #     headers=headers,
            #     formdata=params, )
        except KeyError as e:
            print('tag_page_parse/KeyError: ', e)

    def js_data_extract(self, response):
        js = response.xpath(
            "//script[contains(text(), 'window._sharedData = ')]/text()"
        ).extract_first()
        start_idx = js.index("{")
        data = json.loads(js[start_idx:-1])
        return data
