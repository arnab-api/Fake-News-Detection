import scrapy


class FakeSpider(scrapy.Spider):
    name = "fake"

    def start_requests(self):
        urls = [
            'http://www.prothomalu.com/'
        ]
        print(" ======> start_requests called")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(" ======> parse_requests called")
        news_links = response.css('h3.entry-title > a::attr(href)').extract()
        for link in news_links:
            print(" ----> " , link)
            yield scrapy.Request(url = link , callback = self.parse_news)
        
#        nxt_page = response.css('a.next::attr(href)').extract_first()
#        if(nxt_page):
#            print(nxt_page)
#            yield scrapy.Request(url = nxt_page , callback = self.parse)
    
    def parse_news(self , response):
        title = response.css('h1.entry-title::text').extract_first()
        news_pera = response.css('div.entry-content > p::text').extract()
        news = ""
        for i in range(len(news_pera)):
            if(i > 0) :
                news += " "
            news += news_pera[i]
        yield {
            'headline': title,
            'body': news
        }