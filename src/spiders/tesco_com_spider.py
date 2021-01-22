import scrapy
import json
import logging

from items.tescocom_item import TescoComItem

class TescoComSpiderSpider(scrapy.Spider):
    name = 'tesco_com_spider'
    # start_urls = ['https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all',
    #               'https://www.tesco.com/groceries/en-GB/shop/pets/cat-food-and-accessories/all']
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all']

    logging.basicConfig(
        filename="log.txt",
        format='%(levelname)s: %(message)s',
        level=logging.WARNING
    )

    def parse(self, response):
        products = response.xpath("//div[@class='flexi-tile']")
        for product in products:
            product_URL = response.urljoin(product.xpath("div/a/@href").extract_first())
            product_id = product.xpath("div[@class='tile-content']/@data-auto-id").extract_first()
            product_dict = dict(p_url=product_URL, p_id=product_id)
            yield response.follow(product_URL, callback=self.parse_product, cb_kwargs=product_dict)

        next_page = response.xpath("//a[@title='Go to results page']/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_product(self, response, p_url, p_id):
        item = TescoComItem()

        product_url = p_url
        product_id = p_id
        product_image_url = (response.xpath
                             ("//div[@class='product-image__container']/img/@src").extract_first().split("?")[0])
        product_title = (response.xpath
                         ("//div[@class='product-details-tile__title-wrapper']//h1//text()").extract_first())
        product_category = response.xpath("//div[@class='breadcrumbs__content']//span//text()").extract()[-1]
        product_price = (response.xpath
                         ("//div[@class='price-control-wrapper']//span[@class='value']//text()").extract_first())
        product_description = response.xpath("//div[@id='product-marketing']//text()").extract_first()
        name_and_address = response.xpath("//div[@id='manufacturer-address']//ul//text()").extract()
        return_address = response.xpath("//div[@id='return-address']//ul//text()").extract()
        net_contents = response.xpath("//div[@id='net-contents']//p//text()").extract()

        # Usually Bought Next Products
        ubnps = response.xpath("//div[@class='recommender__wrapper']//div[@class='product-tile-wrapper']")
        ubnps_dict = {}
        for ubnp in ubnps:
            ubnp_product_uri = ubnp.xpath("div//a[@class='product-image-wrapper']/@href").extract_first()
            ubnp_product_url = response.urljoin(ubnp_product_uri)
            ubnp_product_title = ubnp.xpath("div//h3//text()").extract_first()
            ubnp_image_url = (ubnp.xpath
                              ("div//img[@class='product-image']/@src").extract_first())
            ubnp_product_price = (ubnp.xpath
                                  ("div//span[@class='value']//text()").extract_first())

            dict_key = product_title + "__ubnp" + str(len(ubnps_dict) + 1)
            ubnps_dict.update({dict_key: {
                                            "ubnp product url": ubnp_product_url,
                                            "ubnp product title": ubnp_product_title,
                                            "ubnp product image url": ubnp_image_url,
                                            "ubnp product price": ubnp_product_price
                                           }
                               })
        ubnps_json = json.dumps(ubnps_dict)

        # Reviews
        reviews = {}
        reviews = self.parse_reviews(response, reviews_dict=reviews)
        reviews_json = json.dumps(reviews)

        item['product_url'] = product_url
        item['product_id'] = product_id
        item['product_image_url'] = product_image_url
        item['product_title'] = product_title
        item['product_category'] = product_category
        item['product_price'] = product_price
        item['product_description'] = product_description
        item['name_and_address'] = "".join(name_and_address).encode("utf-8")
        item['return_address'] = "".join(return_address).encode("utf-8")
        item['net_contents'] = "".join(net_contents).encode("utf-8")
        item['reviews'] = reviews_json
        item['ubnps'] = ubnps_json

        yield item

    def parse_reviews(self, response, reviews_dict=dict()):
        reviews = response.xpath("//article/section")
        for review in reviews:
            review_title = review.xpath("h4//text()").extract_first()
            review_stars_count = review.xpath("div//span//text()").extract_first()
            review_author = review.xpath("p//text()").extract()[0]
            review_date = review.xpath("p//text()").extract()[1]
            review_text = review.xpath("p//text()").extract()[2]
            reviews_dict[len(reviews_dict)+1] = [review_title,
                                                 review_stars_count,
                                                 review_author,
                                                 review_date,
                                                 review_text]

        next_page_reviews = (response.urljoin
                             (response.xpath("//a[contains(@class, 'beans-link__anchor')]/@href").extract()[-1]))
        if next_page_reviews:
            pass
        return reviews_dict
