# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import selenium
import sqlite3

class DaumCSpider(CrawlSpider):
    name = 'daum_c'
    allowed_domains = ['movie.daum.net']
    # start_urls = ['https://movie.daum.net/premovie/released?opt=reserve&page=1',
    #               'https://movie.daum.net/premovie/released?opt=reserve&page=2',
    #               'https://movie.daum.net/premovie/released?opt=reserve&page=3']

    start_urls=['https://movie.daum.net/premovie/scheduled?opt=reserve&page=1',
                'https://movie.daum.net/premovie/scheduled?opt=reserve&page=2',
                'https://movie.daum.net/premovie/scheduled?opt=reserve&page=3',
                'https://movie.daum.net/premovie/scheduled?opt=reserve&page=4',
                'https://movie.daum.net/premovie/scheduled?opt=reserve&page=5',
                'https://movie.daum.net/premovie/scheduled?opt=reserve&page=6']

    rules = (
        Rule(LinkExtractor(allow=r'https://movie.daum.net/moviedb/main\?movieId=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://movie.daum.net/moviedb/main\?movieId=*'))
    )

    def parse_item(self, response):
        item = {}
        item['movie_img'] = list(response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/span/a/img').xpath("@src").extract())[0]
        item['movie_name'] = response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/strong/text()').extract()
        item['movie_name_e'] = response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/span/text()').extract()
        item['movie_director'] = list(response.xpath(
            '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dd[1]/a//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/dl[1]/dd[4]/a/text()').extract())
        item['movie_actor'] = list(response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/dl[1]/dd[5]/a/text()').extract())
        item['movie_cate'] = response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/dl[1]/dd[1]/text()').extract()
        item['movie_age'] = ''
        item['movie_date'] = response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/dl[1]/dd[3]/text()').extract()

        item['movie_score'] = response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/a/em/text()').extract()
        item['movie_content'] = response.xpath(
            '//*[@id="mArticle"]/div[2]/div[2]/div[1]/div[1]/div[3]/p/text()').extract()
        item['reple_score']=list(response.xpath(
            '//*[@id="mainGradeDiv"]/ul/li[1]/div/div[1]/em/text()').extract())
        item['reple_content']=list(response.xpath(
            '//*[@id="mainGradeDiv"]/ul/li[1]/div/p').extract())

        item['movie_site']='daum'


        return item
    def store_rep(self, name, dire, rep, score, site):
        try:

            result=self.cursor.execute('''select Mov_code from Mov_info where Mov_name_kor=? and Mov_director like "%?%";''',(str(name),str(dire)))
            code=result.fetchone()
            self.cursor.execute(
                '''insert into Mov_score (Mov_code, Rep_cont,Rep_score,Rep_site, Add_date) values (?,?,?,?, datetime())''',
                (str(code), str(rep), str(score), str(site)))

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