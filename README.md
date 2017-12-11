# scrapy框架的使用实例3

* [极客学院](#极客学院)
    * [地址](#地址)
    * [item编写](#item编写)
    * [spider编写](#spider编写)
* [百度贴吧](#百度贴吧)
    * [地址](#地址)
    * [item编写](#item编写)
    * [spider编写](#spider编写)
* [豆瓣电影](#豆瓣电影)
    * [地址](#地址)
    * [item编写](#item编写)
    * [spider编写](#spider编写)
* [mongodb的使用](#mongodb的使用)
    * [地址](#地址)
    * [相关下载](#相关下载)
    * [item编写](#item编写)
    * [spider编写](#spider编写)
    * [pipeline编写](#pipelines编写)
    * [setting设置](#settings设置)
* [redis的使用](#redis的使用)
    * [相关下载](#相关下载)
    * [注意事项](#注意事项)
    

## 极客学院

### 地址
[http://www.jikexueyuan.com/course/](http://www.jikexueyuan.com/course/)

### item编写
```
class JikeItem(scrapy.Item):
    name = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    difficulty = scrapy.Field()
    peoples = scrapy.Field()
```
### spider编写
```
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
```


## 百度贴吧

### 地址
[http://tieba.baidu.com/p/3522395718](http://tieba.baidu.com/p/3522395718)

### item编写
```
class BaiduTieba(scrapy.Item):
    username = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
```

### spider编写
```
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
```


## 豆瓣电影

### 地址
[https://movie.douban.com/top250](https://movie.douban.com/top250)

### item编写
```
class DoubanItem(scrapy.Item):
    movie_name = scrapy.Field()
    movie_intro = scrapy.Field()
    movie_director = scrapy.Field()
    movie_starring = scrapy.Field()
    people_num = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    evaluation = scrapy.Field()
```

## spider编写
```
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
```


## mongodb的使用

### 地址
[http://www.daomubiji.com](http://www.daomubiji.com)

### 相关下载
1. mongoDB安装
  
需要下载mongoDB数据库程序，进行安装，然后会获取到一个安装的文件夹。  
默认安装在
```
C:\Program Files\MongoDB\Server\3.4\bin
```
首先可以手动创建data文件夹和data下的db文件夹  
打开命令行启动mongoDB服务器  
```
mongod --dbpath ./data/db
```
为了方便可以创建批处理start.bat,里面的代码上面的一句启动即可  
成功命令行会保持开启状态  
需要注意的是：c盘下的文件夹权限设置，没有全选可能导致开启服务失败  

2. robomongo的安装

robomongo是mongodb的可视化界面，方便对mongodb的相关操作  

3. pymongo安装

python中mongodb的操作需要安装pymongo，可以使用pip命令
```
pip install pymongo
```

### item编写
```
class NovelspiderItem(scrapy.Item):
    bookName = scrapy.Field()
    bookTitle = scrapy.Field()
    chapterNum = scrapy.Field()
    chapterName = scrapy.Field()
    chapterDetail = scrapy.Field()
    chapterUrl = scrapy.Field()
```

### spider编写
```
# _*_ coding:utf-8 _*_
import scrapy
from ScrapyCode03Dawn.items import NovelspiderItem
from ScrapyCode03Dawn.pipelines import NovelspiderPipeline


class NovelSpider(scrapy.Spider):
    pipeline = set([NovelspiderPipeline, ])
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
```

### pipeline编写
```
class NovelspiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        if spider.name == 'novel':
            bookInfo = dict(item)
            self.post.insert(bookInfo)
        return item
```
需要注意的是多个spider和pipeline关联
可以在pipelines中pipeline类的process_item方法的返回spider参数的名称
来判断当前的spider类和pipeline类的关联

### setting设置
在settings.py中配置MongoDB的IP地址，端口号，数据记录名称，可以实现方便的更换MongoDB的数据库信息  
在settings.py中引用pipelines.py从而使pipelines生效  
在pipelines中可以像普通的Python文件操作MongoDB一样编写代码处理需要保存到MongoDB的数据。
然而不同的是这里的数据来自items。这样做的好处是将数据的抓取和处理分开。  
```
ITEM_PIPELINES = {'ScrapyCode03Dawn.pipelines.NovelspiderPipeline':300}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
COOKIES_ENABLED = True

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'dawn'
MONGODB_DOCNAME = 'Book'
```

## redis的使用

### 相关下载
1. redis的安装

下载redis程序，安装到本地，默认路径是
```
C:\Program Files\Redis
```

2. RedisDesktopManager安装

redis的可视化程序，可以对redis的相关操作

3. scrapy_redis安装

scrapy中的redis使用需要安装scrapy_redis,使用pip
```
pip install scrapy_redis
```

### 注意事项
运行出错，应该是setting配置出现问题，暂时没发现，保留