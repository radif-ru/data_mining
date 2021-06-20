import json
import time
from pathlib import Path
import requests


# # url = "https://5ka.ru/special_offers/"
# url = "https://5ka.ru/api/v2/special_offers/"
# params = {
#     "store": "363H"
# }
# headers = {
#     "User-Agent": "Philip Kirkorov"
# }
# response = requests.get(url, params=params, headers=headers)
#
# tmp_file = Path(__file__).parent.joinpath("tmp.htm")
#
# # tmp_file.write_bytes(response.content)
# #
# data = response.json()
#
# print(1)

class Parse5ka:
    headers = {
        "User-Agent": "Philip Kirkorov"
    }

    def __init__(self, start_url, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            file_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, file_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data['results']:
                yield product

    def _save(self, data, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False),
                             encoding='utf-8')


class Parse5kaCategories(Parse5ka):
    def __init__(self, start_url, save_path: Path, category):
        super().__init__(start_url, save_path)

        self.parent_group_name = category['parent_group_name']
        self.params = {"categories": category['parent_group_code']}

    def _get_response(self, url):
        while True:
            response = requests.get(
                url,
                headers=self.headers,
                params=self.params)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        products = {"name": parent_group_name,
                    "code": self.params['categories'],
                    "products": []}
        for product in self._parse(self.start_url):
            products["products"].append(product)
        file_path = self.save_path.joinpath(
            f"{self.parent_group_name}.json")
        self._save(products, file_path)

    def _parse(self, url):
        response = self._get_response(url)
        data: dict = response.json()
        for product in data['results']:
            yield product


def get_save_path(dir_name: str) -> Path:
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == '__main__':
    # url = "https://5ka.ru/api/v2/special_offers/"
    # product_path = get_save_path('products')
    # parser = Parse5ka(url, product_path)
    # parser.run()

    url = "https://5ka.ru/api/v2/categories/"
    headers = {
        "User-Agent": "Philip Kirkorov"
    }

    response = requests.get(url, headers=headers)
    categories = response.json()

    url = "https://5ka.ru/api/v2/special_offers/"
    product_path = get_save_path('products_by_category')
    for category in categories:
        parent_group_code = category['parent_group_code']
        parent_group_name = category['parent_group_name']

        params = {
            "categories": parent_group_code
        }

        product_path = get_save_path('products_by_category')
        parser = Parse5kaCategories(url, product_path, category)
        parser.run()
