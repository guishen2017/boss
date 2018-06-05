# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BossItem(scrapy.Item):
    position_name = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    work_experience = scrapy.Field()
    education = scrapy.Field()
    tags = scrapy.Field()
    describes = scrapy.Field()
    company_describe = scrapy.Field()
    information = scrapy.Field()
    work_location = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
