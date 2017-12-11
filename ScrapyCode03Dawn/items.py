# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapycode03DawnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JikeItem(scrapy.Item):
    name = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    difficulty = scrapy.Field()
    peoples = scrapy.Field()


class BaiduTieba(scrapy.Item):
    username = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()


class DoubanItem(scrapy.Item):
    movie_name = scrapy.Field()
    movie_intro = scrapy.Field()
    movie_type = scrapy.Field()
    people_num = scrapy.Field()
    star_num = scrapy.Field()


class NovelspiderItem(scrapy.Item):
    bookName = scrapy.Field()
    bookTitle = scrapy.Field()
    chapterNum = scrapy.Field()
    chapterName = scrapy.Field()
    chapterDetail = scrapy.Field()
    chapterUrl = scrapy.Field()