# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingItem(scrapy.Item):
    item_img = scrapy.Field()
    item_company = scrapy.Field()
    item_title = scrapy.Field()
    item_price = scrapy.Field()
    item_sort = scrapy.Field()
    item_info1= scrapy.Field()
    item_info2= scrapy.Field()
    pass
