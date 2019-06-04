# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ItemCrawlSpider(CrawlSpider):
    name = 'auction_crwal'
    allowed_domains = ['itempage3.auction.co.kr']

    def __init__(self, keyword=None, *args, **kwargs):
        super(ItemCrawlSpider, self).__init__(*args, **kwargs)
        keyword.replace(' ','+')
        self.start_urls = ['http://browse.auction.co.kr/search?keyword=%s&p=1' %keyword]
        print(self.start_urls)

    rules = (
        Rule(
            LinkExtractor(allow=r'DetailView\.aspx\?itemno=*'),
            callback='parse_item',
            follow=True),
        Rule(LinkExtractor(allow=r'DetailView\.aspx\?itemno=*'))
    )

    def parse_item(self, response):
        i = {}
        i['item_img'] = list(response.xpath(
            '//*[@id="content"]/div[2]/div[1]/div/div/ul/li/a/img').xpath("@src").extract())[0]
        print(i['item_img'])
        i['item_title'] = response.xpath(
            '//*[@id="frmMain"]/h1/span/text()').extract()
        i['item_price'] = response.xpath(
            '//*[@id="frmMain"]/div[2]/div[1]/div/span/strong/text()').extract()
        return i
