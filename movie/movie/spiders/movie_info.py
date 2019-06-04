# -*- coding: utf-8 -*-
import re
import sqlite3

from scrapy.spiders import CrawlSpider


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
        # img = str('http://www.kobis.or.kr/kobis/business/mast/mvie/popupImg.do?imgURL=') + list(response.xpath(
        img = ''.join(list(response.xpath(
            '//*/div/div[1]/div[2]/a/img').xpath("@src").extract())[0])
        name = ' '.join(response.xpath(
            '/html/body/div[3]/div[1]/div[1]/div/strong/text()').extract())
        name_e = ' '.join(response.xpath(
            '/html/body/div[3]/div[1]/div[1]/div/text()').extract())
        # date = ' '.join(response.xpath(
        #     '//*/div/div[1]/div[2]/dl/dd/text()').extract())
        # '//*[@id="ui-id-181"]/div/div[1]/div[2]/dl/dd[6]'
        date = ' '.join(response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[5]/text()|//*/div/div[1]/div[2]/dl/dd[6]/text()').extract())

        info = ' '.join(response.xpath(
            '//*/div/div[1]/div[2]/dl/dd[4]/text()').extract())
        dire = list(response.xpath(
            '//*/dd/a/text()').extract())

        actor = ' '.join(list(response.xpath(
            '//*/dl/div[2]/dd/table/tbody/tr/td/a/text()').extract()))
        cont = ' '.join(response.xpath(
            '//*/div/div[1]/div/p/text()').extract())

        self.store_data(code, img, name, name_e, date, info, dire, actor, cont)

    def parse(self, response):
        itemList = []
        print(
            "-------------------------------------------------------------------------------------------------------")
        print(len(self.responseList))
        print(
            "-------------------------------------------------------------------------------------------------------")
        for response in self.responseList:
            item = {}
            # codes = map(int,response.xpath(
            #     '//*/div/div[1]/div[2]/dl/dd[1]/text()').extract())
            # for i in codes:
            #     code=i
            #
            # print(type(code))
            code = ' '.join(response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[1]/text()').extract())
            # img = str('http://www.kobis.or.kr/kobis/business/mast/mvie/popupImg.do?imgURL=') + list(response.xpath(
            img = ' '.join(list(response.xpath(
                '//*/div/div[1]/div[2]/a/img').xpath("@src").extract())[0])
            name = ' '.join(response.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/strong/text()').extract())
            name_e = ' '.join(response.xpath(
                '/html/body/div[3]/div[1]/div[1]/div/text()').extract())
            # date = ' '.join(response.xpath(
            #     '//*/div/div[1]/div[2]/dl/dd/text()').extract())
            # '//*[@id="ui-id-181"]/div/div[1]/div[2]/dl/dd[6]'
            date = ' '.join(response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[dt/text()="개봉일"]/text()').extract())
            '//*[@id="ui-id-181"]/div/div[1]/div[2]/dl/dd[6]'
            info = ' '.join(response.xpath(
                '//*/div/div[1]/div[2]/dl/dd[4]/text()').extract())
            dire = list(response.xpath(
                '//*/dd/a/text()').extract())
            actor = ' '.join(list(response.xpath(
                '//*/dl/div[2]/dd/table/tbody/tr/td/a/text()').extract()))
            cont = ' '.join(response.xpath(
                '//*/div/div[1]/div/p/text()').extract())

            # self.store_data(code, img, name, name_e, date, info, dire, actor, cont)
        yield itemList

    def store_data(self, code, img, name, name_e, date, info, dire, actor, cont):
        try:
            #self.cursor.execute(
            #    '''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Add_date) values ('''  + str(code) + ',' + str(name) + ',' + str(name_e) + ',' + str(date) + ',' + str(dire) + ',' + str(actor) + ',' + str(info) + ',' + str(cont)  + ''', datetime());''')
            self.cursor.execute('''insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Mov_img, Add_date) values (?,?,?,?,?,?,?,?,?, datetime())''',
                                (str(code),self.strclean(str(name)),self.strclean(str(name_e)),self.cleandate(self.strclean(str(date))),str(dire),str(actor),self.strclean(str(info)),str(cont),self.strclean(str(img))))
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
        except IndexError:
            print('index의 값을 가져올 수 없습니다.')
            pass
        except sqlite3.IntegrityError:
            print('키가 중복되는게 있당.')
            pass

    def strclean(self,stri):
#         stri = str(stri).strip().replace(' ', '').replace('	', '').replace('''
# ''','')
        stri=re.sub('\s','',stri)
        return stri

    def cleandate(self,string):
        re.sub('(\d{4})-(\d{2})-(\d{2})',
               r'\1-\2-\3',
               string)
        return string