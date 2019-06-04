# -*- coding: utf-8 -*-
import scrapy
import re
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
        code = ' '.join(response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[1]/text()').extract())

        img = ''.join(list(response.xpath(
            '//*/div/div[1]/div[2]/a/img').xpath("@src").extract())[0])
        name = ' '.join(response.xpath(
            '/html/body/div[3]/div[1]/div[1]/div/strong/text()').extract())
        name_e = ' '.join(response.xpath(
            '/html/body/div[3]/div[1]/div[1]/div/text()').extract())
        year='20'
        date='해당정보없음'
        date1 = response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[5]/text()').extract()
        date2 = response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[6]/text()').extract()
        date3 = response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[7]/text()').extract()

        if year in date1[0]:
            date = date1[0]

        elif year in date2[0]:
            date = date2[0]

        elif year in date3[0]:
            date = date3[0]


        info = ' '.join(response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[4]/text()').extract())
        dire = ','.join(list(response.xpath(
            '//*/dd/a/text()').extract()))

        actor = ','.join(list(response.xpath(
            '//*/dl/div[2]/dd/table/tbody/tr/td/a/text()').extract()))
        cont = ' '.join(response.xpath(
            '//*/div/div[1]/div/p/text()').extract())
        dir=dire.split(',')

        self.store_data(code, img, name, name_e, date, info, dire, actor, cont)
        #self.update_dir(code,dire)
    def parse(self, response):
        itemList = []

        yield itemList

    def store_data(self, code, img, name, name_e, date, info, dire, actor, cont):

        try:
            self.cursor.execute(
                '''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Mov_img, Add_date) values (?,?,?,?,?,?,?,?,?, datetime())''',
                (str(code), self.strclean(str(name)), self.strclean(str(name_e)),
                 self.cleandate(self.strclean(str(date))), str(dire), str(actor), self.strclean(str(info)),
                 str(cont).strip(),
                 self.strclean(str(img))))

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
        except selenium.common.exceptions.StaleElementReferenceException:
            print('셀리니움 오류당')
            pass

    def update_dir(self, code, dire):
        try:
            self.cursor.execute(
                '''update Mov_info set Mov_director=? where Mov_code=?''',
                (str(dire), str(code)))

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
        except selenium.common.exceptions.StaleElementReferenceException:
            print('셀리니움 오류당')
            pass

    def strclean(self, stri):
        #         stri = str(stri).strip().replace(' ', '').replace('	', '').replace('''
        # ''','')
        stri = re.sub('\s', '', stri).replace('해당정보없음', '')
        return stri

    def cleandate(self, string):
        re.sub('(\d{4})-(\d{2})-(\d{2})',
               r'\1-\2-\3',
               string)
        return string
