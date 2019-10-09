# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Music_comment(scrapy.Item):
    music_url = scrapy.Field()
    title = scrapy.Field()
    song_user = scrapy.Field()
    save_time = scrapy.Field()
    com_time = scrapy.Field()
    star = scrapy.Field()
    com_user = scrapy.Field()
    comment = scrapy.Field()


