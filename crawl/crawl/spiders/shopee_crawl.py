import scrapy
from scrapy_splash import SplashRequest
from crawl.items import ShopeeItem

class ShopeeCrawlSpider(scrapy.Spider):
    name = "shopee_crawl"
    allowed_domains = ["fptshop.vn"]
    start_urls = ['https://fptshop.com.vn/']
    
    render_script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(5))

            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """ 

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse, 
                endpoint='render.html',
                args={
                    'wait': 5,
                    'lua_source': self.render_script,
                }
            )
    
    def parse(self, response):
        item = ShopeeItem()
        
        for product in response.css("div.cdt-product__info"):
            item["product_name"] = product.css("h3 ::text").extract_first()
            item["price_present"] = product.css("div.cdt-product__show-promo > div.progress ::text, div.price ::text").extract_first()
            item["price_old"] = product.css("div.strike-price ::text").extract_first()
            
            yield item 
