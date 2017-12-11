# _*_ coding:utf-8 _*_
import scrapy
from ScrapyCode03Dawn.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def start_requests(self):
        urls = []
        for i in range(1,11):
            url = scrapy.Request("https://movie.douban.com/top250?start=%s&filter=" % (i-1)*25)
            urls.append(url)
        return urls

    def parse(self, response):
        items = []
        lis = response.xpath('//div[@class="article"]/ol[@class="grid_view"]/li')
        for li in lis:
            item = DoubanItem()
            item['movie_name'] = li.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span/text()')[0].extract()
            item['movie_type'] = li.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]/p/text()')[0].extract()
            item['star_num'] = li.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                                        '/div[@class="star"]/span[2]/text()')[0].extract()
            item['people_num'] = li.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]'
                                          '/span[last()]/text()').re('\d+')[0]
            item['movie_intro'] = li.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="bd"]'
                                        '/p[last()]/span[@class="inq"]/text()')[0].extract()
            items.append(item)
        return items