# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import re

class MoviePipeline(object):
    def __init__(self):
        print(
            "-------------------------------------------------------------------------------------------------------")
        print('이닛시작')
        print(
            "-------------------------------------------------------------------------------------------------------")
        self.connection = sqlite3.connect('../movie.db')
        self.cursor = self.connection.cursor()

    def store_data(self, name, dire, rep, score, site):
        try:

            result=self.cursor.execute('''select Mov_code from Mov_info where Mov_name_kor=? and Mov_director like "%?%";''')
            self.cursor.execute(
                '''insert into Mov_score (Mov_code, Mov_name_kor, Mov_director,Rep_cont,Rep_score,Rep_site, Add_date) values (?,?,?,?,?,?, datetime())''',
                (str(result[0]), self.strclean(str(name)), str(dire), str(rep), str(score), str(site)))

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
        #         stri = str(stri).strip().replace(' ', '').replace('	', '').replace('''
        # ''','')
        stri = re.sub('\s', '', stri).replace('해당정보없음', '')
        return stri

    def cleandate(self, string):
        re.sub('(\d{4})-(\d{2})-(\d{2})',
               r'\1-\2-\3',
               string)
        return string
    def process_item(self, item, spider):
        pass
        return item