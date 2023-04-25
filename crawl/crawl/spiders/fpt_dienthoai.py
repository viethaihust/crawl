import scrapy
from scrapy_splash import SplashRequest
from crawl.items import FPTItem

class FptDienthoaiSpider(scrapy.Spider):
    name = "fpt_dienthoai"
    allowed_domains = ["fptshop.com.vn"]
    CATEGORIES = ['dien-thoai', 'may-tinh-xach-tay', 'may-tinh-bang', 'may-tinh-de-ban']
    start_urls = ["http://fptshop.com.vn/may-tinh-bang"]

    render_script = '''
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(2))

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

        assert(splash:wait(2))
        assert(splash:runjs("document.querySelector('div.cdt-product--loadmore > a').click()"))
        assert(splash:wait(2))
        
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
                endpoint="render.html",
                args={
                    'wait': 5,
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        item = FPTItem()
        for product in response.css("div.cdt-product"):
            item["product_name"] = product.css("h3 ::text").extract_first()
            item["price_present"] = product.css("div.cdt-product__show-promo > div.progress ::text, div.price ::text").extract_first()
            item["price_old"] = product.css("div.strike-price ::text").extract_first()
            item['image'] = product.css("div.cdt-product__img img::attr(src)").extract_first()
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
