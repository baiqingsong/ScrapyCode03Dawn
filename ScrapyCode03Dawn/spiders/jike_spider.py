# _*_ coding:utf-8 _*_
import scrapy
from ScrapyCode03Dawn.items import JikeItem


class JikeSpider(scrapy.Spider):
    name = "jike"
    allowed_domains = ["jikexueyuan.com"]
    start_urls = ["http://www.jikexueyuan.com/course/"]

    def start_requests(self):
        reqs = []
        for i in range(1, 5):
            req = scrapy.Request("http://www.jikexueyuan.com/course/?pageNum=%s" % i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        lis = response.xpath('//div[@class="lesson-list"]/ul[@class="cf"]/li')
        items = []
        for li in lis:
            try:
                item = JikeItem()
                item['name'] = li.xpath('.//h2[@class="lesson-info-h2"]/a/text()')[0].extract()
                item['detail'] = li.xpath('.//div[@class="lesson-infor"]/p/text()')[0].extract()
                time = li.xpath('.//div[@class="timeandicon"]/div[@class="cf"]/dl/dd[@class="mar-b8"]/em/text()')[0].extract()
                item['time'] = time.replace('\n', '').replace(' ', '')
                item['difficulty'] = li.xpath('.//div[@class="cf"]/dl/dd[@class="zhongji"]/em/text()')[0].extract()
                item['peoples'] = li.xpath('.//div[@class="cf"]/em[@class="learn-number"]/text()').re('\d+')[0]
                items.append(item)
            except Exception,e:
                print "item error:",e
        return items