import scrapy


class ProthomalospiderSpider(scrapy.Spider):
    name = 'kaler_kantho'
    root = 'http://kalerkantho.com/'
#    allowed_domains = ['http://m.prothomalo.com/']
#    start_urls = ['http://m.prothomalo.com/']
    
    def start_requests(self):
        urls = [
            'http://kalerkantho.com/'
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
    
    def get_topic_name(self , url):
        topic = url.strip().split("/")
        return topic[len(topic)-1]

    def parse(self, response):
        print(" ======> parse_requests called")
        topic_links = response.css('ul.dropdown-menu > li > div > div > div > ul > li > a::attr(href)').extract()
        for link in topic_links:
            # print(" ===> " , link)
            if(self.verify_link(link)): 
                print(" ----> " , link)
                yield scrapy.Request(url = link , callback = self.parse_a_topic_first_page)
    
    def parse_a_topic_first_page(self , response):
        print(" ====> First Page")
        news_links = response.css('div.col-xs-12 > a::attr(href)').extract() #laster ta next page
        nxt_page = news_links[len(news_links) - 1]
        news_links = news_links[0:len(news_links) - 1]
        for link in news_links:
            url = self.build_url(link)
            print(" ----> " , url)
            yield scrapy.Request(url = url , callback = self.parse_news)
        
        print(" ===================> " , nxt_page)
        yield scrapy.Request(url = self.build_url(nxt_page) , callback = self.parse_a_topic)
        
    def build_url(self , url):
        if(self.verify_link(url)):
            return url
        url = url.replace("./" , 'http://kalerkantho.com/')
        return url

    def get_next_page(self , page_links , page_texts):
        for i in range(len(page_links)):
            if(page_texts[i] == '>'):
                return page_links[i]
        return -1

    def parse_a_topic(self , response):
        news_links = response.css('div.col-xs-12 > a::attr(href)').extract() #laster ta next page
        for link in news_links:
            url = self.build_url(link)
            print(" ----> " , url)
            yield scrapy.Request(url = url , callback = self.parse_news)
        
        page_links = response.css('div.paginatorcustom > a::attr(href)').extract()
        page_texts = response.css('div.paginatorcustom > a::text').extract()

        nxt_page = self.get_next_page(page_links , page_texts)
        if(nxt_page != -1):
            print(" ===================> " , nxt_page)
            yield scrapy.Request(url = self.build_url(nxt_page) , callback = self.parse_a_topic)
        
    
    def parse_news(self , response):
        title = response.css('h2::text').extract_first()
        news_pera = response.css('div.some-class-name2 > p::text').extract()
        news = ""
        for i in range(len(news_pera)):
            if(i > 0) :
                news += " "
            news += news_pera[i].strip()
        yield {
            'headline': title,
            'body': news
        }
