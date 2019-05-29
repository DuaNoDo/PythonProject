# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sqlite3

class NaverCSpider(CrawlSpider):
    name = 'naver_c'
    allowed_domains = ['movie.naver.com']
    start_urls = ['https://movie.naver.com/movie/running/current.nhn']

    rules = (
        Rule(LinkExtractor(allow=r'/movie/bi/mi/basic\.nhn\?code=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/bi/mi/point\.nhn\?code=*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/movie/bi/mi/detail\.nhn\?code=*'), callback='parse_item', follow=True)

    )

    def parse_item(self, response):
        item = {}
        item['movie_title'] = response.xpath( '//*[@id="content"]/div[1]/div[2]/div[1]/h3/a[1]/text()').extract()
        item['movie_title_e'] = response.xpath('//*[@id="content"]/div[1]/div[1]/div[2]/h3/strong/text()').extract()
        item['movie_score'] = response.xpath('//*[@id="actualPointPersentBasic"]/div/span/span/text()').extract()
        item['movi_content'] = response.xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div/div[1]/p/text()').extract()
        item['reple_score'] = list(response.xpath( '//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[1]/em/text()').extract())
        item['reple_content'] = list(response.xpath('//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[4]/ul/li/div[2]/p/text()').extract())
        item['movie_site']='naver'

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