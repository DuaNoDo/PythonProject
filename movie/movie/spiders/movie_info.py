# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import selenium
import sqlite3


class MovieInfoSpider(CrawlSpider):
    name = 'movie_info'
    responseList = []
    start_urls = ['http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do']

    def __init__(self):
        print(
            "-------------------------------------------------------------------------------------------------------")
        print('이닛시작')
        print(
            "-------------------------------------------------------------------------------------------------------")
        self.connection = sqlite3.connect('../movie.db')
        self.cursor = self.connection.cursor()

    def addInfoResponse(self, response):
        self.responseList.append(response)

    def parse(self, response):
        itemList = []
        for response in self.responseList:
            item = {}
            item['movie_code'] = response.xpath(
                '//*[@id="ui-id-3"]/div/div[1]/div[2]/dl/dd[1]/text()').extract()
            item['movie_img'] = str('http://www.kobis.or.kr/kobis/business/mast/mvie/popupImg.do?imgURL=')+list(response.xpath(
                '//*/div/div[1]/div[2]/a/img').xpath("@src").extract())[0]
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
            print(
                "11111111111111111111111-------------------------------------------------------------------------------------------------------")
            print(item['movie_img'])
            print(
                "-------------------------------------------------------------------------------------------------------")
            self.store_data(item)
        yield itemList

    def store_data(self, item):
        print(
            "22222222222222222222-------------------------------------------------------------------------------------------------------")
        print(item['movie_img'])
        print(
            "-------------------------------------------------------------------------------------------------------")
        self.cursor.execute('select * from Mov_info')
        #sql='''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Mov_img, Add_date) values (?,?,?,?,?,?,?,?,?, datetime())'''
        # data=(item['movie_code'], item['movie_name'], item['movie_title_e'], item['movie_date'],
        #         item['movie_director'], item['movie_actor'], item['movie_info'], item['movi_content'],
        #         item['movie_img'])
        # self.cursor.execut(sql,data)
        self.connection.commit()
        print(
            "-------------------------------------------------------------------------------------------------------")
        print(str(item['movie_name']) + ' : 입력완료!!')
        print(
            "-------------------------------------------------------------------------------------------------------")
