from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

path = 'C:/Users/won/Desktop/PythonProject/chromedriver.exe'
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(chrome_options=options, executable_path=path)


class MovieSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MovieDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if request.url != 'http://www.megabox.co.kr/?menuId=movie':
            return None

        driver.get(request.url)
        more_button=driver.find_element_by_xpath('//*[@id="moreMovieList"]')

        # while more_button:
        #     more_button.click()
        #     driver.implicitly_wait(50)
        #
        #     print("-------------------------------------------------------------------------------------------------------")
        #     print(more_button)
        #     print("-------------------------------------------------------------------------------------------------------")
        for i in range(0,3):
            more_button.click()
            driver.implicitly_wait(50)


        movie_list = driver.find_element_by_xpath('//*[@id="movieList"]').find_elements_by_tag_name('li')
        # print("-------------------------------------------------------------------------------------------------------")
        # print(movie_list)
        # print("-------------------------------------------------------------------------------------------------------")
        responseList=[]

        #for num in range(0, len(movie_list) ):
        for num in range(0, 5):
            element = driver.find_element_by_xpath('//*[@id="movieList"]/li[' + str(num + 2) + ']/div[1]/div[2]/a')
            driver.execute_script("arguments[0].click();", element)
            driver.implicitly_wait(100)

            responseList.append(
                HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request))

            exitel = driver.find_element_by_xpath('//*[@id="movie_detail"]/div/div/button')
            driver.execute_script("arguments[0].click();", exitel)
            driver.implicitly_wait(100)
            r = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request)
            # print("input: ", r)
            # return r

            #
            # responseList.append(HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request))
            # print("-------------------------------------------------------------------------------------------------------")
            # print(responseList)
            # print("-------------------------------------------------------------------------------------------------------")
        return None


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
