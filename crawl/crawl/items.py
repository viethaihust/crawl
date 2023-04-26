# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlItem(scrapy.Item):
    product_name = scrapy.Field()
    price_present = scrapy.Field()
    price_old = scrapy.Field()
    rate_average = scrapy.Field()
    pass

class ShopeeItem(scrapy.Item):
    product_name = scrapy.Field()
    price_present = scrapy.Field()
    price_old = scrapy.Field()
    pass

class FPTItem(scrapy.Item):
    product_name = scrapy.Field()
    price_present = scrapy.Field()
    price_old = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()
    pass