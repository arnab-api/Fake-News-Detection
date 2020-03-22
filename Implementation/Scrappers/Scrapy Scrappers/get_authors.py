# -*- coding: utf-8 -*-
import scrapy


class GetAuthorsSpider(scrapy.Spider):
    name = 'get_authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        
        auth_urls = response.css('div.quote > span > a::attr(href)').extract()
        for auth in auth_urls:
            url = response.urljoin(auth)
            print(" ---> " , url)
            yield scrapy.Request(url = url , callback = self.parse_author)


        nxt_page = response.css('li.next > a::attr(href)').extract_first()
        print(" ==============> " , nxt_page)
        if(nxt_page):
            nxt_page_url = response.urljoin(nxt_page)
            yield scrapy.Request(url = nxt_page_url , callback = self.parse)

    def parse_author(self , response):

        data = {
            'name' : response.css('h3.author-title::text').extract_first().strip() ,
            'birth_date' : response.css('div.author-details > p > span.author-born-date::text').extract_first()
        }
        yield data