import scrapy
from scrapy_splash import SplashRequest
from crawl.items import ShopeeItem

class ShopeeCrawlSpider(scrapy.Spider):
    name = "shopee_crawl"
    allowed_domains = ["shopee.vn"]
    start_urls = ['https://shopee.vn/%C4%90i%E1%BB%87n-Tho%E1%BA%A1i-Ph%E1%BB%A5-Ki%E1%BB%87n-cat.11036030']
    
    render_script = '''
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(5))

        local num_scrolls = 10
        local scroll_delay = 1

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )

        for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
            end
        end


        
        return {
            html = splash:html(),
            url = splash:url(),
        }
    end
        '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                meta={
                    "splash": {
                        "endpoint": "execute",
                        "args": {
                            'wait': 5,
                            'url': url,
                            "lua_source": self.render_script,
                        },
                    }
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        item = ShopeeItem()
        for product in response.css("div.shopee-search-item-result__item"):
            item["product_name"] = product.css("div._1yN94N ::text").extract_first()
            item["price_present"] = product.css("div.du3pq0 ::text").extract_first()
            yield item

        yield SplashRequest(
            url=response.url,
            callback=self.parse,
            meta={
                "splash": {
                    "endpoint": "execute",
                    "args": {
                        'wait': 5,
                        'url': response.url,
                        "lua_source": self.render_script,
                    },
                }
            },
            dont_filter=True
        )
