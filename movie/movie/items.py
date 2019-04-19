# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    movie_img = scrapy.Field()
    movie_name = scrapy.Field()
    movie_name_e = scrapy.Field()
    movie_content = scrapy.Field()
    movie_director = scrapy.Field()
    movie_actor = scrapy.Field()
    movie_cate = scrapy.Field()
    movie_age = scrapy.Field()
    movie_date = scrapy.Field()
    pass
