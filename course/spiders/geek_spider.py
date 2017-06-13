# -*- coding: utf-8 -*-
# from scrapy.http import Request
# import re
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider
from course.items import GeekItem


class GeekSpider(CrawlSpider):
    # class GeekSpider(RedisSpider):  # use redis
    name = 'geek'
    redis_key = 'geek:start_urls'
    start_urls = ['http://www.jikexueyuan.com/course/python/?pageNum={}'.format(i) for i in range(1, 5)]

    def parse(self, response):
        selector = Selector(response)
        couse_name = selector.xpath('//div[@class="sortMode"]/h1/text()').extract()[0]
        item = GeekItem()
        for sel in selector.xpath('//div[@class="lesson-infor"]'):
            item['title'] = sel.xpath('h2/a/text()').extract()
            item['desc'] = sel.xpath('p/text()').extract()
            item['link'] = sel.xpath('h2/a/@href').extract()
            item['course_name'] = couse_name
            yield item  # 提交给pipeline处理

# filename = re.sub('[^/]*\?.*', '', response.url).split("/")
# filenames = filename[2] + '_' + filename[-1]
