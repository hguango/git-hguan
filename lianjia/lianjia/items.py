# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    locality = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    housetype = scrapy.Field()
    floorspace = scrapy.Field()
    roomarea = scrapy.Field()
    floor = scrapy.Field()
    elevator = scrapy.Field()  # 电梯
    unitprice = scrapy.Field()  # 单价
    totalprice = scrapy.Field()  # 总价
    servicelife = scrapy.Field()  # 房屋年限
    propertyrigtht = scrapy.Field()  # 产权年限
    concerns = scrapy.Field()
    lookers = scrapy.Field()
    publishtime = scrapy.Field()
