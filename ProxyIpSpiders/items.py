# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpItem(scrapy.Item):
    IP = scrapy.Field()
    PORT = scrapy.Field()
    POSITION = scrapy.Field()
    ANONYMOUS = scrapy.Field()
    TYPE = scrapy.Field()
    SPEED = scrapy.Field()
    LINK_TIME = scrapy.Field()
    TTL = scrapy.Field()
    TTL_MINUTES = scrapy.Field()
    LAST_CHECK_TIME = scrapy.Field()
