# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QianchengwuyouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobName = scrapy.Field()
    jobType = scrapy.Field()
    company = scrapy.Field()
    companyType = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    workingExp = scrapy.Field()
    eduLevel = scrapy.Field()
    welfare = scrapy.Field()
    timestate = scrapy.Field()
    detail = scrapy.Field()

    pass
