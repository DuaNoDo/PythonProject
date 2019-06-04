# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sqlite3
import re

class NaverCSpider(CrawlSpider):
    name = 'naver_c'
    allowed_domains = ['movie.naver.com']
    start_urls = ['https://movie.naver.com/movie/running/current.nhn']
    connection = sqlite3.connect('../movie.db')
    cursor = connection.cursor()

    rules = (
        Rule(LinkExtractor(allow=r'/movie/bi/mi/basic\.nhn\?code=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/bi/mi/point\.nhn\?code=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/bi/mi/detail\.nhn\?code=*'), callback='parse_item', follow=True)

    )

    def parse_item(self, response):

        item = {}
        item['movie_title'] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a[1]/text()').extract()
        item['movie_title_e'] = response.xpath('//*[@id="content"]/div[1]/div[1]/div[2]/h3/strong/text()').extract()
        item['movie_director'] = response.xpath(
            '//*[@id="content"]/div[1]/div[1]/div[2]/div[2]/dl[1]/dd/a/text()').extract()
        item['movie_score'] = response.xpath('//*[@id="actualPointPersentBasic"]/div/span/span/text()').extract()
        item['movi_content'] = response.xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div/div[1]/p/text()').extract()
        item['reple_score'] = list(
            response.xpath('//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[1]/em/text()').extract())
        item['reple_content'] = list(
            response.xpath('//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[2]/p/text()').extract())
        item['reple_date']=list(
            response.xpath('//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[2]/dl/dt/em[2]/text()').extract())
        item['movie_site'] = 'naver'
        for i in range (0,len(item['reple_score'])):

            self.store_rep(item['movie_title'], item['movie_director'], item['reple_content'][i], item['reple_score'][i],
                           item['movie_site'],item['reple_date'][i])
        self.store_score(item['movie_title'],item['movie_director'],item['movie_score'][0])
        return item

    def store_rep(self, name, dire, rep, score, site,date):
        try:
            name=name[0]
            name=self.strclean(name)
            dire=dire[0]
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
                    '''insert into Mov_score (Mov_code, Rep_cont,Rep_score,Rep_site,Rep_date, Add_date) values (?,?,?,?,?, datetime())''',
                    (str(code[0]), str(rep), str(score), str(site),str(date)))

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
    def store_score(self, name, dire, score):
        try:
            name=name[0]
            name=self.strclean(name)
            dire=dire[0]
            score=score.replace('관람객 평점 ','').replace('점','')
            result = self.cursor.execute(
                '''select Mov_code from Mov_info where Mov_name_kor=? and Mov_director like  '%' ||?|| '%';''',
                (name, dire))
            code = result.fetchone()
            if code:
                self.cursor.execute(
                    '''update Mov_info set Mov_score_naver =? where Mov_code=?''',
                    (str(score),str(code[0])))

            self.connection.commit()
        except IndexError:
            print('index의 값을 가져올 수 없습니다.')
            pass
        except sqlite3.IntegrityError:
            print('키가 중복되는게 있당.')
            pass

    def strclean(self, stri):
        str = re.sub('\s', '', stri)
        return str
