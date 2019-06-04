import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sqlite3
import re

class MovieCSpider(CrawlSpider):
    name = 'movie_c'
    allowed_domains = ['www.cgv.co.kr']
    start_urls = ['http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=1',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=2',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=3',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=4',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=5',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=6',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=7',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=8',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=9',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=10',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=11',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=12',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=13',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=14',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=15',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=16',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=17',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=18',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=19',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=20',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=21',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=22',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=23',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=24',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=25',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=26',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=27',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=28',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=29',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=30',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=31',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=32',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=33',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=34',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=35',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=36',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=37',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=38',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=39',
                  'http://www.cgv.co.kr/movies/finder.aspx?s=true&sdate=2015&edate=2020&page=40']
    connection = sqlite3.connect('../movie.db')
    cursor = connection.cursor()
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
        item['movie_score']=response.xpath('//*[@id="select_main"]/div[2]/div[2]/div[2]/div/span[2]/text()').extract()
        item['reple_content']=list(response.xpath('//*[@id="movie_point_list_container"]/li/div[3]/p/text()').extract())

        item['reple_score']=list(response.xpath('//*[@id="movie_point_list_container"]/div[2]/ul/li[1]/a/span').extract())

        item['movie_site'] = 'cgv'

        for i in range(0, len(item['reple_score'])):
            score=self.f(item['reple_score'][i])

            print(item)
            self.store_rep(item['movie_name'], item['movie_director'], item['reple_content'][i],
                           score,
                           item['movie_site'])
        self.store_score(item['movie_name'], item['movie_director'],item['movie_score'][0].replace('%',''))
        return item
    def store_rep(self, name, dire, rep, score, site):
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
                    '''update Mov_info set Mov_score_cgv =? where Mov_code=?''',
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

    def f(self,x):
        return {' egg-icon good ': '5', ' egg-icon ': '1'}.get(x, '3')
