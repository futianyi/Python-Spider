# -*- coding: utf-8 -*-
import scrapy
from python123demo.items import Python123DemoItem

class MzSpider(scrapy.Spider):

    name = 'mz'
    allowed_domains = ["www.mzitu.com"]


    def start_requests(self):
        headers = {'Referer': 'http://www.mzitu.com/mm/'}
        #关于urls,'http://www.mzitu.com/xinggan/page/i'其中i代表页数
        #由于1页包含24组图片,1组包含多张图片,因而只是爬取第一页
        #若要爬取多页,使用格式化并迭代或其他有效方法
        urls = [
            'http://www.mzitu.com/xinggan/'
        ]
        for url in urls:
            #要使用yield要在函数里面
            yield scrapy.Request(url=url, headers=headers, method='GET',callback=self.parse)


    def parse(self, response):
        headers = {'Referer': 'http://www.mzitu.com/xinggan/'}
        #li[position()<11]表示前10个li标签,即前10组图片
        li = response.xpath('//div[@class="postlist"]/ul/li[position()<11]')
        for href in li:
            #后面一定要加[0],否则url不是字符串是列表list类型...
            url = href.xpath('./a/@href').extract_first()
            yield scrapy.Request(url, headers=headers, callback=self.group_pictures_url)


    def group_pictures_url(self, response):
        headers = {
            'Referer': 'http://www.mzitu.com/xinggan/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        #extract_first()等同于extract()[0]
        page = response.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()').extract_first()
        n = int(page) + 1
        ##注意把page先变成int类
        for i in range(1, n):
            ##不知道为什么第一张始终下不到,经过检验发现只要是range(1, n),其中n是变量
            #又或者说不是具体的10,20这样的数字,第一张图就下不到,而具体的数字则可以
            newurl = response.url if i==1 else response.url + '/' + str(i)
            yield scrapy.Request(newurl, headers=headers, callback=self.img)

    def img(self,response):

        name = response.css('.main-image p a img::attr(alt)').extract()[0]
        imgurl = response.css('.main-image p a img::attr(src)').extract()[0]
        item = Python123DemoItem()
        item['name'] = name
        item['imgurl'] = imgurl
        yield item








