# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MovieCSpider(CrawlSpider):
    name = 'movie_c'
    allowed_domains = ['movie.naver.com']
    start_urls = ['https://movie.naver.com/movie/running/current.nhn']

    rules = (
        Rule(LinkExtractor(allow=r'/movie/bi/mi/basic\.nhn\?code=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/bi/mi/point\.nhn\?code=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/bi/mi/detail\.nhn\?code=*'), callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        item = {}
        item['movie_img'] = list(response.xpath(
            '//*[@id="content"]/div[1]/div[2]/div[2]/a/img').xpath("@src").extract())[0]
        item['movie_title'] = response.xpath(
            '//*[@id="content"]/div[1]/div[2]/div[1]/h3/a[1]/text()').extract()
        item['movie_title_e'] = response.xpath(
            '//*[@id="content"]/div[1]/div[1]/div[2]/h3/strong/text()').extract()
        item['movie_score'] = response.xpath(
            '//*[@id="actualPointPersentBasic"]/div/span/span/text()').extract()
        item['movi_content'] = response.xpath(
            '//*[@id="content"]/div[1]/div[4]/div[1]/div/div[1]/p/text()').extract()
        item['movie_maker'] = list(response.xpath(
            '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[2]/p/a/text()').extract())
        item['movie_actor'] = list(response.xpath(
            '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[3]/p/a/text()').extract())
        item['reple_score'] = list(response.xpath(
            '//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[1]/em/text()').extract())
        item['reple_content'] = list(response.xpath(
            '//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[2]/p/text()').extract())

        return item
