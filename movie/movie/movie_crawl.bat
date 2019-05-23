@echo off
scrapy crawl movie_c -o cgv.csv -t csv
scrapy crawl daum_c -o daum.csv -t csv
scrapy crawl naver_c -o naver.csv -t csv
scrapy crawl megabox_c -o mega.csv -t csv

