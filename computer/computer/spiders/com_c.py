# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ComCSpider(CrawlSpider):
    name = 'com_c'
    allowed_domains = ['https://www.amazon.com']

    def __init__(self, keyword='cpu', *args, **kwargs):
        super(ComCSpider, self).__init__(*args, **kwargs)
        keyword.replace(' ','+')
        self.start_urls = ['https://www.amazon.com/s?k=%s&page=1' %keyword]
        print(self.start_urls)

    rules = (
        Rule(
            LinkExtractor(allow=r'cr2\.shopping\.naver\.com/adcr\.nhn\?x=*'),
            callback='parse_item',
            follow=True),
        Rule(LinkExtractor(allow=r'cr2\.shopping\.naver\.com/adcr\.nhn\?x=*'))
    )

    def parse_item(self, response):
        i = {}
        i['item_img'] = list(response.xpath(
            '//*[@id="viewImage"]').xpath("@src").extract())[0]
        i['item_company'] = response.xpath(
            '//*[@id="p//*[@id="container"]/div[1]/div[2]/div/div[2]/div[1]/span[1]/em/text()').extract()
        i['item_title'] = response.xpath(
            '//*[@id="container"]/div[1]/div[2]/div/div[1]/h2/text()').extract()
        i['item_price'] = response.xpath(
            '//*[@id="_mainSummaryPrice"]/div[1]/span/em/text()').extract()
        i['item_sort'] = response.xpath(
            '//*[@id="container"]/div[1]/div[1]/div/div[1]/span[3]/a/text()').extract()
        i['item_info1']=response.xpath(
            '//*[@id="container"]/div[1]/div[2]/div/div[2]/div[2]/[span[1]/text()="인텔-코어 : "]').extract()
        i['item_info2'] = response.xpath(
            '//*[@id="container"]/div[1]/div[2]/div/div[2]/div[2]/[span[2]/text()="코어 형태 : "]').extract()

        return i