# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    movie_img = scrapy.Field()
    movie_title = scrapy.Field()
    movie_title_e=scrapy.Field()
    movie_score = scrapy.Field()
    movie_content=scrapy.Field()
    movie_maker=scrapy.Field()
    reple_star=scrapy.Field()
    reple_content=scrapy.Field()
    pass
