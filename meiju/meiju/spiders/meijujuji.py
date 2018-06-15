# -*- coding: utf-8 -*-
from scrapy import Spider
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import sys

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
