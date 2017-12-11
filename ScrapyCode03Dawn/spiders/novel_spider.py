# _*_ coding:utf-8 _*_
import scrapy
from ScrapyCode03Dawn.items import NovelspiderItem


class NovelSpider(scrapy.Spider):
    name = "novel"
    start_urls = ["http://www.daomubiji.com"]

    def parse(self, response):
        # fileName = "result.txt"
        # with open(fileName, "wb") as f:
        #     f.write(response.body)
        articles = response.xpath('//article[@class="article-content"]/div[@class="homebook"]')
        bookName = response.xpath('//h1[@class="focusbox-title"]/text()')[0].extract()
        for i, article in enumerate(articles):
            item = NovelspiderItem()
            item['bookName'] = bookName
            try:
                item['chapterUrl'] = response.xpath('//article[@class="article-content"]'
                                                    '//a[contains(@href, "http://www.daomubiji.com")]/@href')[i].extract()
            except Exception, e:
                print "地址没找到"
            item['bookTitle'] = article.xpath('.//h2/text()')[0].extract()
            item['chapterDetail'] = article.xpath('.//p[@class="homedes"]/text()')[0].extract()
            yield item