# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ItemCrawlSpider(CrawlSpider):
    name = '11street_crawl'
    allowed_domains = ['www.11st.co.kr']

    def __init__(self, keyword=None, *args, **kwargs):
        super(ItemCrawlSpider, self).__init__(*args, **kwargs)
        keyword.replace(' ','+')
        self.start_urls = ['http://search.11st.co.kr/Search.tmall?kwd=%s#pageNum##\d' %keyword]
        print(self.start_urls)

    rules = (
        Rule(
            LinkExtractor(allow=r'product/SellerProductDetail\.tmall\?method=getSellerProductDetail&prdNo=*'),
            callback='parse_item',
            follow=True),
        Rule(LinkExtractor(allow=r'product/SellerProductDetail\.tmall\?method=getSellerProductDetail&prdNo=*'))
    )

    def parse_item(self, response):
        i = {}
        i['item_img'] = list(response.xpath(
            '//*[@id="thumb"]/div[1]/span/img').xpath("@src").extract())[0]
        print(i['item_img'])
        i['item_title'] = response.xpath(
            '//*[@id="productInfoMain"]/div[2]/div[2]/h2/text()').extract()
        i['item_price'] = response.xpath(
            '//*[@id="prdcInfoColumn2"]/div[1]/div[1]/span[2]/span[2]/s/text()').extract()

        return i
