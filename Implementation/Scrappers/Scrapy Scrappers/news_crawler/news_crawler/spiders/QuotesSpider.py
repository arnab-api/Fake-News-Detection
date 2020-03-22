import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        quotes = response.css('div.quote')
        for qt in quotes:
            data = {
                'quote' : qt.css('span.text::text').extract_first(),
                'author' : qt.css('small.author::text').extract_first(),
                'tags' : qt.css('a.tag::text').extract()
            }
            yield data

        nxt_page = response.css("li.next > a::attr(href)").extract_first()
        if(nxt_page):
            url = response.urljoin(nxt_page)
            yield scrapy.Request(url = url , callback = self.parse)