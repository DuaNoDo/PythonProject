# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import selenium
import sqlite3
import re

class MegaboxCSpider(CrawlSpider):
    name = 'megabox_c'
    responseList = []
    start_urls = ['http://www.megabox.co.kr/?menuId=movie']
    connection = sqlite3.connect('../movie.db')
    cursor = connection.cursor()
    def addResponse(self, response):
        self.responseList.append(response)

    def parse(self, response):
        itemList = []
        for response in self.responseList:
            item = {}
            # item["movie_name"] = "123"
            item['movie_img'] = list(response.xpath(
                '//*[@id="movieDetail"]/div[1]/div[1]/img').xpath("@src").extract())[0]
            item['movie_name'] = response.xpath(
                '//*[@id="movieDetail"]/div[1]/div[2]/div[1]/h2/span/text()').extract()
            item['movie_title_e'] = response.xpath(
                '//*[@id="movieDetail"]/div[1]/div[2]/div[1]/p/text()').extract()
            item['movie_director']=response.xpath('//*[@id="movieDetail"]/div[1]/div[2]/div[2]/ul/li[3]/text()').extract()
            item['movie_score'] = response.xpath(
                '//*[@id="averageScoreDetail_015422"]/text()').extract()
            item['movi_content'] = response.xpath(
                '//*[@id="movieDetail"]/div[2]/div/text()').extract()
            item['reple_score'] = list(response.xpath(
                '//*[@id="movieCommentList"]/div/div[1]/div/div[2]/div[2]/div/span/span/span/text()').extract())
            item['reple_content'] = list(response.xpath(
                '//*[@id="movieCommentList"]/div/div[1]/div/div[2]/p/span/text()').extract())
            item['movie_site'] = 'megabox'


            for i in range(0, len(item['reple_score'])):
                self.store_rep(item['movie_name'], item['movie_director'], item['reple_content'][i],
                               item['reple_score'][i],
                               item['movie_site'])
            itemList.append(item)

        return itemList

    def store_rep(self, name, dire, rep, score, site):
        try:
            name=name[0]
            name=self.strclean(name)

            dire=dire[0].split(',')
            dire=dire[0].strip().replace(': ','').replace(':  ','')
            print(
                "-------------------------------------------------------------------------------------------------------")
            print(dire)
            print(
                "-------------------------------------------------------------------------------------------------------")
            result = self.cursor.execute(
                '''select Mov_code from Mov_info where Mov_name_kor=? and Mov_director like  '%' ||?|| '%';''',
                (name, dire))
            # result = self.cursor.execute(
            #     "select Mov_code from Mov_info where Mov_name_kor=?",[name])
            code = result.fetchone()
            print(code)
            if code:
                self.cursor.execute(
                    '''insert into Mov_score (Mov_code, Rep_cont,Rep_score,Rep_site, Add_date) values (?,?,?,?, datetime())''',
                    (str(code[0]), str(rep), str(score), str(site)))

            self.connection.commit()
            print(
                "-------------------------------------------------------------------------------------------------------")
            print(
                "-------------------------------------------------------------------------------------------------------")
        except IndexError:
            print('index의 값을 가져올 수 없습니다.')
            pass
        except sqlite3.IntegrityError:
            print('키가 중복되는게 있당.')
            pass


    def strclean(self, stri):
        str = re.sub('\s', '', stri)
        return str
