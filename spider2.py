class TescoOfferSpider(Spider):
    def getTescoStartUrl():
        tesco_start_url = []
        r = requests.get('https://www.tesco.com/groceries/en-GB/promotions/alloffers')
        data = lxml.html.fromstring(r.text)
        # output = data.xpath('//span[@class="items-count-filter-caption"]/text()')
        output = data.xpath('//div[@class="items-count__filter-caption"]//text()')
        itemcount = output[3].split(' ')
        print(math.ceil(int(itemcount[0]) / 24))
        #    return math.ceil(int(itemcount[0])/24)
        maxpage = math.ceil(int(itemcount[0]) / 24)
        tescourl = 'https://www.tesco.com/groceries/en-GB/promotions/alloffers?page=%d'
        for i in range(1, maxpage):
            tesco_start_url.append(tescourl % i)
        return tesco_start_url
    name = "tescooffer" # Name of the spider, to be used when crawling
    allowed_domains = ["tesco.com"] # Where the spider is allowed to go
    start_urls = getTescoStartUrl()

    def parse(self, response):
        hxs = Selector(response)  # The XPath selector
        # XPath Tags
        productlist_tag = '//div[@class="product-lists"]//ul[@class="product-list grid"]/li'
        product_id_tag = './/div[@class="product-tile--wrapper"]//div[@class="tile-content"]/a/@href'
        product_imgsrc_tag = './/img/@src'
        product_desc_tag = './/div[@class="product-details--wrapper"]//a/text()'
        offer_desc_tag = './/li[@class="product-promotion"]//span[@class="offer-text"]/text()'
        validity_desc_tag = './/li[@class="product-promotion"]//span[@class="dates"]/text()'
        offertags = hxs.xpath(productlist_tag)
        ###

        tescooffers = []
        for offertag in offertags:
            offer = TescoOfferItem()
            offer['productid'] = offertag.xpath(product_id_tag).extract()[0].replace("/groceries/en-GB/products/","")
            if offertag.xpath(product_imgsrc_tag).extract():
                offer['imgsrc225'] = offertag.xpath(product_imgsrc_tag).extract()[0]
                offer['imgsrc110'] = offertag.xpath(product_imgsrc_tag).extract()[0].replace('225x225','110x110')
                offer['imgsrc90'] = offertag.xpath(product_imgsrc_tag).extract()[0].replace('225x225','90x90')
                offer['imgsrc540'] = offertag.xpath(product_imgsrc_tag).extract()[0].replace('225x225','540x540')
            else:
                offer['imgsrc90'] = ""
                offer['imgsrc540'] = ""
                offer['imgsrc110'] = ""
                offer['imgsrc225'] = ""
            if offertag.xpath(product_desc_tag).extract():
                offer['productdesc'] = offertag.xpath(product_desc_tag).extract()[0]
            else:
                offer['productdesc'] = ""
            if offertag.xpath(offer_desc_tag).extract():
                offer['offerdesc'] = offertag.xpath(offer_desc_tag).extract()[0]
            else:
                offer['offerdesc'] = ""
            if offertag.xpath(validity_desc_tag).extract():
                offer['validitydesc'] = offertag.xpath(validity_desc_tag).extract()[0]
            else:
                offer['validitydesc'] = ""
            tescooffers.append(offer)
        return tescooffers # To be changed later
