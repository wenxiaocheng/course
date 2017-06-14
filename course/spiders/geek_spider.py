# -*- coding: utf-8 -*-
from scrapy.http import Request
# import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import Request
from course.items import GeekItem


# class GeekSpider(CrawlSpider):
class GeekSpider(RedisCrawlSpider):  # use redis
    name = 'geek'
    redis_key = 'geek:start_urls'
    start_urls = ['https://www.cnblogs.com/',
                  'http://www.jikexueyuan.com/course/']

    rules = (
        Rule(LinkExtractor(allow=(r'www.jikexueyuan.com/course/[\u4e00-\u9fa5_a-zA-Z0-9]+/')), callback='parse_item'),
        Rule(LinkExtractor(allow=(r'www.cnblogs.com')), callback='parse_item'),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse_item(self, response):
        selector = Selector(response)
        couse_name = selector.xpath('//div[@class="sortMode"]/h1/text()').extract()
        item = GeekItem()
        for sel in selector.xpath('//div[@class="lesson-infor"]'):
            item['title'] = sel.xpath('h2/a/text()').extract()
            item['desc'] = sel.xpath('p/text()').extract()
            item['link'] = sel.xpath('h2/a/@href').extract()
            item['course_name'] = couse_name
            yield item  # 提交给pipeline处理

            # def parse(self, response):
            #     selector = Selector(response)
            #     type_urls = selector.xpath('//dd[@class="cf"]/a/@href').extract()
            #     urls = ['http:{}'.format(url) for url in type_urls]
            #     for url in urls:
            #         yield Request(url, callback='parse_item')

            # filename = re.sub('[^/]*\?.*', '', response.url).split("/")
            # filenames = filename[2] + '_' + filename[-1]

            # rules = (
            #     Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="lesson-info-h2"]/a@href',)), callback='parse_item'),
            # )

            # lpush geek:start_urls http://www.jikexueyuan.com/course/python/?pageNum=1
