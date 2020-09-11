import scrapy
import re
from Tachie_get.items import *


class ForWhomTheGoldSpider(scrapy.Spider):
    name = 'for_whom_the_gold'
    allowed_domains = ['wiki.fwg.mobage.cn', 'static.mobage.cn']
    start_urls = ['http://wiki.fwg.mobage.cn/units?page_num=0']

    def parse(self, response):
        char_li = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/table/tbody/tr')
        for i in char_li:
            item = TachieGetItem()
            item['name'] = i.xpath('./td[1]/a/p/text()').extract_first()
            url = i.xpath('./td[1]/a/@href').extract_first()
            char_url = 'http://wiki.fwg.mobage.cn' + url
            # 发送角色详情页的请求，使用回调函数接收响应
            yield scrapy.Request(
                url=char_url,
                callback=self.get_tachie_url,
                meta={'item':item}  # 使用meta在不同函数中传递参数
            )

        last_page = 13  # 由于要爬取网页的特殊性，即倒数第二页与最后一页的href属性均指向最后一页，所以采用了另一种方法，13为最后一页的页码
        next_url = response.xpath(
            '/html/body/div[2]/div/div[2]/div[2]/a[3]/@href').extract_first()  # 从“下一页”button中获取下一页的url地址，注意若不使用extractfirst()方法则返回值为一个列表
        now_page = response.xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[1]/a[@class="current"]/text()').extract_first()  # 获取当前页面的页码

        # 判断是否到达尾页
        if int(now_page) < last_page:
            next_url = 'http://wiki.fwg.mobage.cn/units' + next_url  # href属性并非完整的url，需要补全域名
            # 使用yield发送请求
            yield scrapy.Request(
                url=next_url,  # 设置下一个url
                callback=self.parse  # 设置回调函数为本身，当然也可以定义一个新函数
            )


    # 处理角色详情页，获取角色立绘url
    def get_tachie_url(self, response):
        item = response.meta['item']
        url = response.xpath('/html/body/div[2]/div/div/div[1]/div[5]/div[1]/img/@src')
        item['img_url'] = url.extract_first()  # 将🖼图片url及后缀保存至item
        print(item['img_url'])
        item['img_class'] = url.extract_first().split('.')[-1]
        yield item

