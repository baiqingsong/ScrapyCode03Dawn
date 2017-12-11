# _*_ coding:utf-8 _*_
import scrapy
from ScrapyCode03Dawn.items import BaiduTieba


class BaiduTiebaSpider(scrapy.Spider):
    name = "baidu_tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ["http://tieba.baidu.com/p/3522395718"]

    def parse(self, response):
        divs = response.xpath('//div[@class="left_section"]/div[@class="p_postlist"]/'
                              'div[contains(@class, "l_post j_l_post l_post_bright")]')
        items = []
        for div in divs:
            item = BaiduTieba()
            item['username'] = div.xpath('.//div[@class="d_author"]/ul[@class="p_author"]/li[@class="d_name"]/a/text()')[0].extract()
            content = div.xpath('.//div[contains(@class,"d_post_content_main")]/'
                                'div[contains(@class, "p_content")]/cc/div/text()')[0].extract()
            item['content'] = content.replace('\n', '').replace(' ', '')
            item['time'] = item['time'] = div.xpath('./@data-field').re('\d{4}-\d{2}-\d{2}*\d{2}:\d{2}')[0]

            items.append(item)
        return items