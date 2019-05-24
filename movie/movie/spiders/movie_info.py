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
            # codes = map(int,response.xpath(
            #     '//*/div/div[1]/div[2]/dl/dd[1]/text()').extract())
            # for i in codes:
            #     code=i
            #
            # print(type(code))
            code = response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[1]/text()').extract()
            # img = str('http://www.kobis.or.kr/kobis/business/mast/mvie/popupImg.do?imgURL=') + list(response.xpath(
            img = list(response.xpath(
                '//*/div/div[1]/div[2]/a/img').xpath("@src").extract())[0]
            name = response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[3]/text()').extract()
            name_e = response.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/text()').extract()
            date = response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[5]/text()').extract()
            info = response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[4]/text()').extract()
            dire = response.xpath(
                '//*/dd/a/text()').extract()
            actor = list(response.xpath(
                '//*/dl/div[2]/dd/table/tbody/tr/td/a/text()').extract())
            cont = response.xpath(
                '//*/div/div[1]/div[5]/p/text()').extract()

            self.store_data(code, img, name, name_e, date, info, dire, actor, cont)
        yield itemList

    def store_data(self, code, img, name, name_e, date, info, dire, actor, cont):
        #self.cursor.execute(
        #    '''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Add_date) values ('''  + str(code) + ',' + str(name) + ',' + str(name_e) + ',' + str(date) + ',' + str(dire) + ',' + str(actor) + ',' + str(info) + ',' + str(cont)  + ''', datetime());''')
        self.cursor.execute('''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Mov_img, Add_date) values (?,?,?,?,?,?,?,?,?, datetime())''',(str(code),str(name),str(name_e),str(date),str(dire),str(actor),str(info),str(cont),str(img)))
        # sql='''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Mov_img, Add_date) values (?,?,?,?,?,?,?,?,?, datetime())'''
        # data=(item['movie_code'], item['movie_name'], item['movie_title_e'], item['movie_date'],
        #         item['movie_director'], item['movie_actor'], item['movie_info'], item['movi_content'],
        #         item['movie_img'])
        # self.cursor.execut(sql,data)
        self.connection.commit()
        print(
            "-------------------------------------------------------------------------------------------------------")
        print(
            "-------------------------------------------------------------------------------------------------------")
