# -*- coding: utf-8 -*-
import scrapy
import json

class ScrollSpider(scrapy.Spider):
    name = 'scroll'
    allowed_domains = ['quotes.toscrape.com']
    api_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api_url.format(1)]

    def parse(self, response):
        data = json.loads(response.text)
        print("called page :: " , data['page']) 
        for quote in data['quotes']:
            yield {
                'author' : quote['author']['name'] , 
                'text' : quote['text'] , 
                'tags' : quote['tags']
            }

        if(data['has_next']):
            nxt_page = data['page'] + 1
            url = self.api_url.format(nxt_page)
            print(url)
            yield scrapy.Request(url = url , callback = self.parse)