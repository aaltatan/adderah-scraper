import logging

import scrapy
from scrapy.http import Request, TextResponse

from .. import items


logging.basicConfig(
    filemode='a',
    filename='logger.log',
    format='[%(asctime)s] %(levelname)s | %(name)s => %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8',
    level=logging.INFO
)


class ItemsSpider(scrapy.Spider):

    name = "items"
    allowed_domains = ["www.adderah.com"]
    start_urls = ["https://www.adderah.com/search/?search="]

    def parse(self, response: TextResponse):

        links = response.css('#product-view .item.single-product .image > a:first-child::attr(href)').getall()
        for link in links:
            yield Request(url=link, callback=self.parse_item)
        
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield Request(next_page, callback=self.parse)

    def parse_item(self, response: TextResponse):

        breadcrumb = response.css('.breadcrumb a::text').getall()
        category, subcategory, *_ = breadcrumb

        description = response.css('#tab-description *::text').getall()

        images = response.css('#gallery img::attr(src)').getall()

        shipping_data: dict = {}
        shipping_items = []

        shipping_rows = response.css('#tab-mm-shipping table tbody tr')

        for row in shipping_rows:
            direction, method, duration, price = row.css('td').getall()
            shipping_data['direction'] = direction
            shipping_data['method'] = method
            shipping_data['duration'] = duration
            shipping_data['price'] = price
            shipping_items.append(items.Shipping(**shipping_data))
        
        item_data = {
            'name': response.css('#page-title::text').get(''),
            'price': response.css('#product-price::text').get(''),
            'seller': response.css('.sellersname::text').get(''),
            'in_stock': response.css('.info.in_stock::text').get(''),
            'images': images,
            'image_urls': images,
            'description': description,
            'category': category,
            'subcategory': subcategory,
            'url': response.url,
        }

        return items.Item(
            **item_data, shipping=shipping_items
        )

