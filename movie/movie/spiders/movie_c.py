# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MovieCSpider(CrawlSpider):
    name = 'movie_c'
    allowed_domains = ['www.cgv.co.kr']
    start_urls = ['http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=1960&edate=2020&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'/movies/detail-view/\?midx=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movies/detail-view/\?midx=*'))
    )

    def parse_item(self, response):
        item = {}
        item['movie_img'] = list(response.xpath(
            '//*[@id="select_main"]/div[2]/div[1]/a/span/img').xpath("@src").extract())[0]
        item['movie_name'] = response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[1]/strong/text()').extract()
        item['movie_name_e'] = response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[1]/p/text()').extract()
        item['movie_director'] = list(response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dd[1]/a/text()').extract())
        item['movie_actor'] = list(response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dd[3]/a/text()').extract())
        item['movie_cate'] = response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dt[3]/text()').extract()
        item['movie_age'] = response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dd[5]/text()').extract()
        item['movie_date'] = response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dt[6]/text()').extract()

        item['movie_content1'] = response.xpath(
            '//*[@id="menu"]/div[1]/div[1]/*/text()').extract()
        item['movie_content2'] = response.xpath(
            '//*[@id="menu"]/div[1]/div[1]/div/*/text()').extract()
        item['movie_content3'] = response.xpath(
            '//*[@id="menu"]/div[1]/div[1]/*//text()').extract()
        item['movie_content4'] = response.xpath(
            '//*[@id="menu"]/div[1]/div[1]//text()').extract()
        item['movie_content5'] = response.xpath(
            '//*[@id="menu"]/div[1]/div[1]//*//text()').extract()

        return item
