美剧爬取
======

## 前言 
我个人特别喜欢看美剧，然而看美剧就要有相应的资源来源，所以我一般在字幕组这个网站下载资源(http://www.zimuzu.tv) 。它的视频资源丰富，而且支持多种下载方式。



![字幕组网站资源示例](https://upload-images.jianshu.io/upload_images/5498924-4b0398b270c03547.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)



但是如果我想下载一整部剧的资源就很麻烦，于是便有了用**Scrapy+Selenium+Mongodb**编写的这个项目，以便于更好的下载资源。



## 网页分析

首先打开网站首页，找到搜索框。

![搜索框](https://upload-images.jianshu.io/upload_images/5498924-a45ef05a88ff5197.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)

在搜索框中输入关键词如西部世
