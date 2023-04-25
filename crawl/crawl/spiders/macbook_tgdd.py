import scrapy

from crawl.items import CrawlItem


class MacbookTgddSpider(scrapy.Spider):
    name = "macbook_tgdd"
    allowed_domains = ["www.thegioididong.com"]
    start_urls = ["http://www.thegioididong.com/"]

    def parse(self, response):
        # Request tới từng sản phẩm có trong danh sách các Macbook dựa vào href
        for item_url in response.css("div.item > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_macbook) # Nếu có sản phẩm thì sẽ gọi tới function parse_macbook
        
       # nếu có sản phẩm kế tiếp thì tiếp tục crawl
        next_page = response.css("div.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    
    def parse_macbook(self, response):
        item = CrawlItem()
        
        item['product_name'] = response.css('section.detail > h1 ::text').extract_first()
        
        item['price_present'] = response.css('p.box-price-present ::text').extract_first()

        item['price_old'] = response.css('p.box-price-old ::text').extract_first()
                            
        item['rate_average'] = response.css('div.rating-top > p.point ::text').extract_first()

        yield item

        pass
