# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TescoComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_url = scrapy.Field()
    product_id = scrapy.Field()
    product_image_url = scrapy.Field()
    product_title = scrapy.Field()
    product_category = scrapy.Field()
    product_price = scrapy.Field()
    product_description = scrapy.Field()
    name_and_address = scrapy.Field()
    return_address = scrapy.Field()
    net_contents = scrapy.Field()
    reviews = scrapy.Field()
    ubnps = scrapy.Field()
