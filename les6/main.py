from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# from gb_parse.spiders.youla import AutoyoulaSpider
# from gb_parse.spiders.hh import HhRemoteSpider
from les6.gb_parse.spiders.avito import AvitoSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    # crawler_process.crawl(AutoyoulaSpider)
    crawler_process.crawl(AvitoSpider, mark='kazan')
    crawler_process.start()
