import scrapy
import requests
import lxml.html
import math
from scrapy.crawler import CrawlerProcess
from scrapy.item import Field
from scrapy.selector import Selector
from urllib.parse import urlsplit, parse_qs


class SainsburysOfferItem(scrapy.Item):
    productid = Field()
    imgsrcl = Field()
    productdesc = Field()
    offerdesc = Field()
    producturl = Field()


class MySpider(scrapy.Spider):
    def getSainsStartUrl():
        sains_start_url = []
        # def build_starturl():
        # categoryId=[12518,13343,267396,267397,12320,218831,12422,12192,12448,11651,12564,12298,281806]
        categoryId = [12518]
        # categoryId=[12518,13343,12422]
        urlstring = 'https://www.sainsburys.co.uk/shop/gb/groceries/home/CategorySeeAllView?langId=44&storeId=10151&catalogId=10123&pageSize=108&facet=88&categoryId=%d&categoryFacetId1=%d&beginIndex=%d'
        for n in categoryId:
            r = requests.get(urlstring % (n, n, 0))
            data = lxml.html.fromstring(r.text)
            output = data.xpath('//h1[@id="resultsHeading"]/text()')
            item = output[0].replace('  ', '').replace('\r\n', '').split('(')[0]
            itemcount = output[0].replace('  ', '').replace('\r\n', '').split('(')[1].split(' ')[0]
            print(item, ':', itemcount)
            for i in range(0, math.ceil(int(itemcount.replace(',', '')) / 108)):
                sains_start_url.append(urlstring % (n, n, i * 108))
                # print(urlstring%(n,n,i*108))
        return sains_start_url

    name = "sainsoffer"  # Name of the spider, to be used when crawling
    allowed_domains = ["sainsburys.co.uk"]  # Where the spider is allowed to go
    start_urls = getSainsStartUrl()

    def parse(self, response):
        hxs = Selector(response)  # The XPath selector
        product_grid = '//div[@id="productsContainer"]/div[@id="productLister"]/ul[contains(@class,"productLister")]//li[@class="gridItem"]'
        product_id_tag = './/div[@class="productInfo"]//div[@class="promotion"]//a/@href'
        offer_desc_tag = './/div[@class="productInfo"]//div[@class="promotion"]//a/text()'
        product_url = './/div[@class="productInfo"]//h3/a/@href'
        product_desc_tag = './/div[@class="productInfo"]//h3/a/text()'
        product_imgsrc_tag = './/div[@class="productInfo"]//h3/a/img/@src'
        offertags = hxs.xpath(product_grid)
        sainsoffers = []

        for offertag in offertags:
            offer = SainsburysOfferItem()
            offer['productid'] = parse_qs(urlsplit(offertag.xpath(product_id_tag).extract()[0]).query)['productId'][0]
            offer['imgsrcl'] = offertag.xpath(product_imgsrc_tag).extract()[0]
            offer['productdesc'] = offertag.xpath(product_desc_tag).extract()[0].replace('  ', '').replace('\r\n', '')
            offer['offerdesc'] = offertag.xpath(offer_desc_tag).extract()[0].replace('  ', '').replace('\r\n', '')
            offer['producturl'] = offertag.xpath(product_url).extract()[0]
            sainsoffers.append(offer)
        return sainsoffers


SETTINGS = {
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEED_URI': 'file:///c:/tmp/python1/test.json',
    'FEED_FORMAT': 'json',
    'DOWNLOAD_DELAY': '5',
    'LOG_LEVEL': 'INFO'
}

process = CrawlerProcess(SETTINGS)
process.crawl(MySpider)
process.start()
