import os

import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gb_parse.spiders.youla import AutoyoulaSpider
from gb_parse.spiders.hh import HhRemoteSpider
from gb_parse.spiders.avito import AvitoRealEstateSpider
from gb_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    dotenv.load_dotenv("gb_parse/spiders/instagram/.env")
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(
        InstagramSpider,
        login=os.getenv('LOGIN'),
        password=os.getenv('PASSWORD'),
        tags=["pugachevaforever", ],
        # tags=["pugachevaforever", "kirkorow", ]
    )
    crawler_process.start()
