# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import selenium


class MegaboxCSpider(CrawlSpider):
    name = 'megabox_c'

    start_urls = ['http://www.megabox.co.kr/?menuId=movie']

    def parse(self, response):
        item = {}
        item["movie_name"] = "123"
        print("parse():", response)
        # item['movie_img'] = list(response.xpath(
        #    '//*[@id="movieDetail"]/div[1]/div[1]/img').xpath("@src").extract())[0]
        # item['movie_name'] = response.xpath(
        #     '//*[@id="movieDetail"]/div[1]/div[2]/div[1]/h2/span/text()').extract()
        # item['movie_title_e'] = response.xpath(
        #    '//*[@id="movieDetail"]/div[1]/div[2]/div[1]/p/text()').extract()
        # item['movie_score'] = response.xpath(
        #    '//*[@id="averageScoreDetail_015422"]/text()').extract()
        # item['movi_content'] = response.xpath(
        #    '//*[@id="movieDetail"]/div[2]/div/text()').extract()
        # item['reple_score'] = list(response.xpath(
        #    '//*[@id="movieCommentList"]/div/div[1]/div[1]/div[2]/div[2]/div/span/span/span/text()').extract())
        # item['reple_content'] = list(response.xpath(
        #    '//*[@id="movieCommentList"]/div/div[1]/div[1]/div[2]/p/span/text()').extract())
        # item['movie_site'] = 'megabox'

        return item
