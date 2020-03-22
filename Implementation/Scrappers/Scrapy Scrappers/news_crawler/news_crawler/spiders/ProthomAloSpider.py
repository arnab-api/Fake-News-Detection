import scrapy


class ProthomalospiderSpider(scrapy.Spider):
    name = 'prothom_alo'
    root = 'http://m.prothomalo.com/'
#    allowed_domains = ['http://m.prothomalo.com/']
#    start_urls = ['http://m.prothomalo.com/']
    
    def start_requests(self):
        urls = [
            'http://m.prothomalo.com/'
        ]
        print(" ======> start_requests called")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def verify_link(self , link):
        if(len(link) < len(self.root)):
            return False
        for i in range(len(self.root)):
            if(self.root[i] != link[i]):
                return False
        return True

    def parse(self, response):
        print(" ======> parse_requests called")
        topic_links = response.css('div.menu > ul > li > a::attr(href)').extract()
        topic_links = topic_links[1:len(topic_links)]
        for link in topic_links:
            print(" ===> " , link)
            if(self.verify_link(link)): 
                print(" ----> " , link)
                yield scrapy.Request(url = link , callback = self.parse_a_topic)
            
    def parse_a_topic(self , response):
        news_links = response.css('div.selected_content_each > a::attr(href)').extract()
        for link in news_links:
            if(self.verify_link(link)): 
                print(" ----> " , link)
                yield scrapy.Request(url = link , callback = self.parse_news)
        
        nxt_page = response.css('a.next_icon::attr(href)').extract()
        if(len(nxt_page) > 0):
            print(" ===================> " , nxt_page)
            yield scrapy.Request(url = nxt_page[0] , callback = self.parse_a_topic)
        
    
    def parse_news(self , response):
        title = response.css('h1.news_title::text').extract_first()
        news_pera = response.css('div.description > p::text').extract()
        news = ""
        for i in range(len(news_pera)):
            if(i > 0) :
                news += " "
            news += news_pera[i]
        yield {
            'headline': title,
            'body': news
        }
