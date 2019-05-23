# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import selenium


class MovieInfoSpider(CrawlSpider):
    name = 'movie_info'
    responseList = []
    start_urls = ['http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do']

    def addInfoResponse(self, response):
        self.responseList.append(response)

    def parse(self, response):
        itemList = []
        for response in self.responseList:
            item = {}
            item['movie_code'] = response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[2]/dl/dd[1]/text()').extract()
            item['movie_img'] = list(response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[2]/a/img').xpath("@src").extract())[0]
            item['movie_name'] = response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[2]/dl/dd[3]/text()').extract()
            item['movie_title_e'] = response.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/text()').extract()
            item['movie_date'] = response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[2]/dl/dd[5]/text()').extract()
            item['movie_info'] = response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[2]/dl/dd[4]/text()').extract()
            item['movie_director'] = response.xpath(
                '//*[@id="20199954_director"]/dd/a/text()').extract()
            item['movie_actor'] = list(response.xpath(
                '//*[@id="20199954_staff"]/dl/div[2]/dd/table/tbody/tr/td/a/text()').extract())
            item['movi_content'] = response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[5]/p/text()').extract()

        return itemList
