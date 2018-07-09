import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.item import Field
from scrapy.selector import Selector
import logging
import json

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MorrisonsOfferItem(scrapy.Item):
    imgsrcl = Field()
    productdesc = Field()
    offerdesc = Field()
    producturl = Field()
    offerurl = Field()
    productprice = Field()
    unitprice = Field()


class MorrisonsSpider(scrapy.Spider):
    def getChildCatUrls():
        categories = ['104268', '102210', '104162', '102705', '103644', '103120', '102063', '166274', '103497', '102838', '166275', '103423', '102207', '150516', '153052']
        # categories = ['104268', '104162']
        # categories = [104268]
        base_url = 'https://groceries.morrisons.com'
        base_cat_url = base_url + '/webshop/subNavigation?catalogueType=OFFER_PRODUCTS&tags=|105651|19998|%s'

        cat_url = {}
        starturls = []

        for category in categories:
            response = requests.get(base_cat_url % category)
            json_obj = json.loads(response.content)
            logger.debug(json_obj)
            for lvl1 in json_obj['categories']:
                if 'children' in lvl1:
                    for child1 in lvl1['children']:
                        if 'children' in child1:
                            for child2 in child1['children']:
                                logger.debug(child2['name'])
                                cat_url[lvl1['name'] + '->' + child1['name'] + '->' + child2['name']] = base_url + child2['url']
                                starturls.append(base_url + child2['url'])
                        else:
                            logger.debug(child1['name'])
                            cat_url[lvl1['name'] + '->' + child1['name']] = base_url + child1['url']
                            starturls.append(base_url + child1['url'])
                else:
                    logger.debug(lvl1['name'])
                    cat_url[lvl1['name']] = base_url + lvl1['url']
                    starturls.append(base_url + lvl1['url'])
        logger.info(json.dumps(cat_url))
        logger.info(starturls)
        return starturls

    name = "morrioffer"  # Name of the spider, to be used when crawling
    allowed_domains = ["morrisons.com"]  # Where the spider is allowed to go
    # start_urls = ['https://groceries.morrisons.com/webshop/getOfferProducts.do?tags=|105651|19998|104268|113925|113955&Asidebar=2']
    start_urls = getChildCatUrls()


    def parse(self, response):
        hxs = Selector(response)
        product_grid = '//div[@id="js-productPageFops"]/ul/li'
        img_src = './/div[@class="fop-item"]//img/@src'
        prod_desc = './/div[@class="fop-item"]//div[@class="fop-description"]/h4[contains(@class,"fop-title")]/text()'
        prod_url = './/div[@class="fop-item"]//div[contains(@class,"fop-content-wrapper")]/a/@href'
        promo_desc = './/div[@class="fop-item"]//a[contains(@class,"fop-row-promo")]/span/text()'
        promo_url = './/div[@class="fop-item"]//a[contains(@class,"fop-row-promo")]/@href'
        price = './/div[@class="fop-item"]//div[@class="price-group-wrapper"]/h5[contains(@class,"fop-price")]/text()'
        unit_price = './/div[@class="fop-item"]//div[@class="price-group-wrapper"]/span[@class="fop-unit-price"]/text()'
        offertags = hxs.xpath(product_grid)

        morrioffers = []
        base_url = 'https://groceries.morrisons.com'
        for offertag in offertags:
            offer = MorrisonsOfferItem()
            offer['imgsrcl'] = base_url + offertag.xpath(img_src).extract_first()
            offer['productdesc'] = offertag.xpath(prod_desc).extract_first().replace('  ', '').replace('\r\n', '').replace('\n', '')
            offer['offerdesc'] = offertag.xpath(promo_desc).extract_first().replace('  ', '').replace('\r\n', '').replace('\n', '')
            offer['producturl'] = base_url + offertag.xpath(prod_url).extract_first()
            offer['offerurl'] = base_url + offertag.xpath(promo_url).extract_first()
            offer['productprice'] = offertag.xpath(price).extract_first().replace('  ', '').replace('\r\n', '').replace('\n', '')
            offer['unitprice'] = offertag.xpath(unit_price).extract_first()
            morrioffers.append(offer)

        return morrioffers


SETTINGS = {
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEED_URI': 'file:///c:/tmp/python1/morris.json',
    'FEED_FORMAT': 'json',
    'DOWNLOAD_DELAY': '2',
    'LOG_LEVEL': 'INFO'
}

process = CrawlerProcess(SETTINGS)
process.crawl(MorrisonsSpider)
process.start()


'''
base_url = 'https://groceries.morrisons.com'

response = requests.get(base_url + '/webshop/getOfferProducts.do')
soup = BeautifulSoup(response.content, 'html.parser')
li1s = soup.find_all('li', class_='CATEGORY')

for li1 in li1s:
    logger.info('Level 1: ' + li1.a.text + ':' + li1.a['href'])
    out1 = requests.get(base_url + li1.a['href'])
    soup1 = BeautifulSoup(out1.content, 'html.parser')
    # lis1 = soup1.findAll('li', {"data-sku": re.compile(r".*")})
    li2s = soup1.findAll('li', class_='CATEGORY')
    for li2 in li2s:
        logger.info('\tLevel 2: ' + li2.a.text + ':' + li2.a['href'])
        out2 = requests.get(base_url + li2.a['href'])
        soup2 = BeautifulSoup(out2.content, 'html.parser')
        li3s = soup2.find_all('li', class_='CATEGORY')
        for li3 in li3s:
            logger.info('\t\tLevel 3: ' + li3.a.text + ':' + li3.a['href'])
'''
'''
        img_src = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//img/@src'
        prod_desc = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//div[@class="fop-description"]/h4[contains(@class,"fop-title")]/text()'
        prod_url = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//div[contains(@class,"fop-content-wrapper")]/a/@href'
        promo_desc = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//a[contains(@class,"fop-row-promo")]/span/text()'
        promo_url = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//a[contains(@class,"fop-row-promo")]/@href'
        price = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//div[@class="price-group-wrapper"]/h5[contains(@class,"fop-price")]/text()'
        unit_price = '//div[@id="js-productPageFops"]/ul/li/div[@class="fop-item"]//div[@class="price-group-wrapper"]/span[@class="fop-unit-price"]/text()'
'''
