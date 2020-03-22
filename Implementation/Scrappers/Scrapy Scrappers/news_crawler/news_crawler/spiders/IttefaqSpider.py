import scrapy


class ProthomalospiderSpider(scrapy.Spider):
    name = 'ittefaq'
    root = 'http://www.ittefaq.com.bd/'
#    allowed_domains = ['http://m.prothomalo.com/']
#    start_urls = ['http://m.prothomalo.com/']
    
    def start_requests(self):
        urls = [
            'http://www.ittefaq.com.bd/'
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
        topic_links = response.css('ul.dropdown > li > a::attr(href)').extract()
        topic_links = topic_links[2:len(topic_links)-1]
        for link in topic_links:
            print(" ===> " , link)
            if(self.verify_link(link)): 
                print(" ----> " , link)
                yield scrapy.Request(url = link , callback = self.parse_a_topic)
    
    def get_next_page_link(self , arr):
        for a in arr:
            img = a.css('img').extract()
            if(len(img) == 0):
                continue
            img = img[0]
            if(img == '<img src="http://www.ittefaq.com.bd/static/version/0.04/images/next-arrow.png">'):
                return a.css('a::attr(href)').extract_first()
        return -1

    def parse_a_topic(self , response):
        news_links = response.css('div.headline > a::attr(href)').extract()
        for link in news_links:
            if(self.verify_link(link)): 
                print(" ----> " , link)
                yield scrapy.Request(url = link , callback = self.parse_news)
        
        arr = response.css('span > a')
        nxt_page = self.get_next_page_link(arr)
        if(nxt_page != -1):
            print(" ===================> " , nxt_page)
            yield scrapy.Request(url = nxt_page , callback = self.parse_a_topic)
        
    
    def parse_news(self , response):
        title = response.css('div.headline2::text').extract_first()
        news_pera = response.css('div.details > div > span::text').extract()
        news = ""
        for i in range(len(news_pera)):
            if(i > 0) :
                news += " "
            news += news_pera[i].strip()
        yield {
            'headline': title,
            'body': news
        }
