# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from lianjia.items import LianjiaItem
from scrapy.http import Request


class SzLianjiaSpider(scrapy.Spider):
    name = 'sz.lianjia'
    allowed_domains = ['sz.ianjia.com']
    start_urls = ['https://sz.lianjia.com/ershoufang/']

    def parse(self, response):
        self._pre_url = 'https://sz.lianjia.com'
        a_html = HtmlXPathSelector(response)
        a_list = a_html.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for l in a_list:
            url = self._pre_url + l
            yield Request(url, callback=self.parse_b, dont_filter=True)
            #break

    def parse_b(self, response):
        b_html = HtmlXPathSelector(response)
        b_list = b_html.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href').extract()
        for l in b_list:
            url = self._pre_url + l
            #yield Request(url, callback=self.parse_c, dont_filter=True)
            #break

    def parse_c(self, response):
        c_html = HtmlXPathSelector(response)
        c_list = c_html.xpath('/html/body/div[4]/div[1]/ul/li[@class="clear"]')
        cur_url = c_html.xpath('//div[@class="contentBottom clear"]/div[1]/h1/a/@href').extract()[0]
        for i in c_list:
            item = LianjiaItem()
            address = i.xpath('div[1]/div[2]/div/a/text()').extract()[0]
            # address = i.xpath('div[1]//div[@class="houseInfo"]/a/text()').extract()
            url = i.xpath('a/@href').extract()[0]
            title = i.xpath('div[1]/div[1]/a/text()').extract()[0]
            extra = i.xpath('div[1]/div[4]/text()').extract()[0]
            concerns = extra.split('/')[0]
            lookers = extra.split('/')[1]
            totalprice = i.xpath('div[1]/div[6]/div[1]/span/text()').extract()[0] +\
                        i.xpath('div[1]/div[6]/div[1]/text()').extract()[0]

            unitprice = i.xpath('div[1]/div[6]/div[2]/span/text()').extract()[0]
            item['url'] = url
            item['title'] = title
            item['concerns'] = concerns
            item['lookers'] = lookers
            item['address'] = address
            item['totalprice'] = totalprice
            item['unitprice'] = unitprice
            item['locality'] = cur_url.split('/')[2]
            yield Request(url, meta={'item': item}, callback=self.parse_item, dont_filter=True)
            #break
        pagenum = c_html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        pagenum = pagenum[1:-1]
        totalPage = int(pagenum.split(',')[0].split(':')[1])
        curPage = int(pagenum.split(',')[1].split(':')[1])
        #print(cur_url)
        #print(totalPage, curPage)
        if curPage < totalPage:
            next_page = self._pre_url + cur_url + 'pg%s' % (curPage + 1)
            print(next_page)
            yield Request(next_page, callback=self.parse_c, dont_filter=True)

    def parse_item(self, response):
        item = response.meta['item']
        b_html = HtmlXPathSelector(response)
        xl = '//*[@id="introduction"]/div/div/div[1]/div[2]/ul/'
        housetype = b_html.xpath(xl + 'li[1]/text()').extract()[0]
        floorspace = b_html.xpath(xl + 'li[3]/text()').extract()[0]
        roomarea = b_html.xpath(xl + 'li[5]/text()').extract()[0]
        floor = b_html.xpath(xl + 'li[2]/text()').extract()[0]
        elevator = b_html.xpath(xl + 'li[11]/text()').extract()[0]
        propertyrigtht = b_html.xpath(xl + 'li[12]/text()').extract()[0]
        xl2 = '//*[@id="introduction"]/div/div/div[2]/div[2]/ul/'
        servicelife = b_html.xpath(xl2 + 'li[5]/span[2]/text()').extract()[0]
        publishtime = b_html.xpath(xl2 + 'li[1]/span[2]/text()').extract()[0]
        item['housetype'] = housetype
        item['floorspace'] = floorspace
        item['roomarea'] = roomarea
        item['floor'] = floor
        item['elevator'] = elevator
        item['propertyrigtht'] = propertyrigtht
        item['servicelife'] = servicelife
        item['publishtime'] = publishtime
        yield item
