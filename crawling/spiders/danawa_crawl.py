# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ItemCrawlSpider(CrawlSpider):
    name = 'danawa_crwal'
    allowed_domains = ['prod.danawa.com']

    def __init__(self, keyword=None, *args, **kwargs):
        super(ItemCrawlSpider, self).__init__(*args, **kwargs)
        keyword.replace(' ','+')
        self.start_urls = ['http://search.danawa.com/dsearch.php?query=%s&page=1' %keyword]
        print(self.start_urls)

    rules = (
        Rule(
            LinkExtractor(allow=r'info/\?pcode=*'),
            callback='parse_item',
            follow=True),
        Rule(LinkExtractor(allow=r'info/\?pcode=*'))
    )

    def parse_item(self, response):
        i = {}
        i['item_img'] = list(response.xpath(
            '//*[@id="baseImage"]').xpath("@src").extract())[0]
        print(i['item_img'])
        i['item_title'] = response.xpath(
            '//*[@id="blog_content"]/div[2]/div[1]/h3/text()').extract()
        i['item_price'] = response.xpath(
            '//*[@id="blog_content"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/span[2]/a/em/text()').extract()
        return i
