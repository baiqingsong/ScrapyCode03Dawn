# _*_ coding:utf-8 _*_
import scrapy


class QqtvSpider(scrapy.Spider):
    name = "qqtv"
    start_urls = ["https://v.qq.com/x/cover/qviv9yyjn83eyfu/u0016gbvtgc.html"]

    def parse(self, response):
        with open("result.txt", "wb") as f:
            f.write(response.body)