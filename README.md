美剧爬取
======

## 前言 
我个人特别喜欢看美剧，然而看美剧就要有相应的资源来源，所以我一般在字幕组这个网站下载资源（http://www.zimuzu.tv）。 它的视频资源丰富，而且支持多种下载方式。



![字幕组网站资源示例](https://upload-images.jianshu.io/upload_images/5498924-4b0398b270c03547.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)



但是如果我想下载一整部剧的资源就很麻烦，于是便有了用**Scrapy+Selenium+Mongodb**编写的这个项目，以便于更好的下载资源。



## 网页分析

首先打开网站首页，找到搜索框。

![搜索框](https://upload-images.jianshu.io/upload_images/5498924-a45ef05a88ff5197.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)

在搜索框中输入关键词如西部世界可以跳转到这个url，注意这里的关键词应为url编码，只不过在网站显示的是中文。

![跳转搜索页面](https://upload-images.jianshu.io/upload_images/5498924-63217559a7a775b8.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)



用开发工具定位到电视剧该标签的url，构造完整url路径，点击并跳转到资源链接页面找到这个模块。

![资源链接模块](https://upload-images.jianshu.io/upload_images/5498924-59bf6aec6a8197db.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)

在此进行网页分析时发现并没有源码，可能是动态显示效果，用Selenium进行定位成功提取到链接，点击模块并跳转到资源下载页。

![资源模块](https://upload-images.jianshu.io/upload_images/5498924-408807fe86e3cdad.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)



接下来我们对标题title和下载方式downloader进行定位，至此就完成了页面分析。



## 编译环境

* Win10操作系统
* Python3.6语言版本
* Google Chrome浏览器
* Pycharm编译软件



## 项目步骤

> * 创建scrapy项目，命名为meiju,创建爬虫文件meijujuji。
> * 调用相关库并进行爬虫程序meijuSpider的编写。
> * 编写MongoDBPipeline以便连接Mongodb数据库。
> * 进行相应的settings设置，运行程序观察数据库结果。
##调用相关库

```python
from scrapy import Spider
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import sys
```


## Spider编写

```python
class meijuSpider(Spider):
    name = 'meijujuji'
    #关键词搜索，如西部世界
    word = input("请输入搜索关键字：")
    #使用psrse方法将关键词转化为url编码
    start_words = parse.quote(word)
    start_urls = ['http://www.zimuzu.tv/search?keyword=' + start_words]

    def parse(self,response):
        #用xpath方式定位到关键词的url
        word_url = response.xpath('//em[text()="电视剧"]/../div[@class="fl-img"]/a/@href').extract()
        process_word = ''.join(word_url)
        #判断url是否存在，不存在直接退出程序
        if process_word=='':
            print("没有找到或输入错误")
            sys.exit(0)
        #构造资源链接页的url
        process_url = 'http://www.zimuzu.tv' + process_word
        #调用Options()方法加载动态解析，设置为不显示浏览器界面
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='E:\京兆人\Python\chromedriver.exe', chrome_options=chrome_options)
        driver.get(process_url)
        #构造资源下载页的url
        last_url = driver.find_element_by_xpath('//div[@id="resource-box"]/div/div/h3/a').get_attribute('href')
        driver.close()

        yield scrapy.Request(last_url,callback = self.parse_meiju)

    def parse_meiju(self, response):
        info = response.xpath('//li[@class="item"]/div[@class="title"]')
        #定义一个字典，抓取title和downloader放进字典中
        Dict = {}

        for i in range(len(info)):
            titles = str(info[i].xpath('span/text()').extract()).strip("[]").replace("'","")
            Dict['title']=titles
            li = info[i].xpath('ul/li | ../ul/li')
            for i in range(len(li)):
                downloader = str(li[i].xpath('a/p/text()').extract()).strip("[]'")
                try:
                    link = str(li[i].xpath('a/@href').extract()).strip("[]'")
                except:
                    link = '--'
                Dict[downloader]=link
            yield Dict

```


## Pipelines编写

```python
#调用pymongo库
from pymongo import MongoClient
#编写MongoDBPipeline
class MongoDBPipeline(object):

    #定义一个从setting读取数据库地址，名称,集合名称的函数
    @classmethod
    def from_crawler(cls,crawler):
        cls.url = crawler.settings.get('MONGODB_DB_URL', 'mongodb://localhost:27017/')
        cls.dbname = crawler.settings.get('MONGODB_DB_NAME', 'default')
        cls.collectionname = crawler.settings.get('MONGODB_COLLECTION_NAME','default')
        return cls()

    #定义插入数据库的函数
    def process_item(self,item,spider):
        #连接数据库
        client = MongoClient(self.url)
        db = client[self.dbname]
        post = db[self.collectionname]
        #将item类型转化为字典类型
        dicts = dict(item)
        post.insert(dicts)
        return item

    #定义数据库连接关闭函数
    def close_spider(self,spider):
        self.client.close()

```


## Settings设置

```python
MONGODB_DB_URL = 'mongodb://localhost:27017/'
MONGODB_DB_NAME = 'meiju'
MONGODB_COLLECTION_NAME = 'juji'

ITEM_PIPELINES = {
   'meiju.pipelines.MongoDBPipeline': 300,
}
```


## 结果展示

打开Mongodb数据库，这里用Studio 3T可视化Mongodb数据库，运行meiju爬虫，输入要查找的美剧如西部世界，成功的获取到了相应的资源。



![](https://upload-images.jianshu.io/upload_images/5498924-3cefabd43800f348.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)




