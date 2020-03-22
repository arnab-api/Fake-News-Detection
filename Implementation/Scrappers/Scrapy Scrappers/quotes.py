# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.log("I just visited :: "+response.url)
        quotes = response.css('div.quote')
        for qt in quotes:
            data = {
                'quote' : qt.css('span.text::text').extract_first(),
                'author' : qt.css('small.author::text').extract_first(),
                'tags' : qt.css('a.tag::text').extract()
            }
            yield data
        next_url = response.css('li.next > a::attr(href)').extract_first()
        if(next_url):
            goto = response.urljoin(next_url)
            yield scrapy.Request(url = goto , callback = self.parse)