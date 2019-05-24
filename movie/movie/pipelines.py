# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class MoviePipeline(object):
    # def __init__(self):
    #     print(
    #         "-------------------------------------------------------------------------------------------------------")
    #     print('이닛시작')
    #     print(
    #         "-------------------------------------------------------------------------------------------------------")
    #     self.connection = sqlite3.connect('../movie.db')
    #     self.cursor = self.connection.cursor()
    #
    # def process_item(self, item, spider):
    #     print(
    #         "-------------------------------------------------------------------------------------------------------")
    #     print('이닛시작')
    #     print(
    #         "-------------------------------------------------------------------------------------------------------")
    #     self.connection = sqlite3.connect('../movie.db')
    #     self.cursor = self.connection.cursor()
    #     self.cursor.execute(
    #         "insert into Mov_info (Mov_code, Mov_name_kor, Mov_name_eng, Mov_date, Mov_director, Mov_actor, Mov_info, Mov_content, Mov_img, Add_date) "
    #         "values (?,?,?,?,?,?,?,?,?, datetime())", (
    #             item['movie_code'], item['movie_name'], item['movie_title_e'], item['movie_date'], item['movie_director'], item['movie_actor'], item['movie_info'], item['movi_content'],item['movie_img']))
    #     self.connection.commit()
    #     print(
    #         "-------------------------------------------------------------------------------------------------------")
    #     print(item['movie_name']+' : 입력완료!!')
    #     print(
    #         "-------------------------------------------------------------------------------------------------------")
    #     return item
    def process_item(self, item, spider):
        pass
        return item