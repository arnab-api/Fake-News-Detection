import scrapy


class MotiSpider(scrapy.Spider):
    name = "fake_moti"
    root = 'https://motikontho.wordpress.com/'

    def start_requests(self):
        urls = [
            'https://motikontho.wordpress.com/'
        ]
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
        news_links = response.css('h2 > a::attr(href)').extract()
        for link in news_links:
            if(self.verify_link(link)): 
                print(" ----> " , link)
                yield scrapy.Request(url = link , callback = self.parse_news)
        
        navigation = response.css('div.navigation > a::attr(href)').extract()
        nav_dsp = response.css('div.navigation > a::text').extract()
        nxt_page = ""
        for i in range(len(nav_dsp)):
            if(nav_dsp[i] == '« Older Entries'):
                nxt_page = navigation[i]
                break

        if(nxt_page != ""):
            print(" ===================> " , nxt_page)
            yield scrapy.Request(url = nxt_page , callback = self.parse)
    
    def parse_news(self , response):
        title = response.css('div.post > h2::text').extract_first()
        news_pera = response.css('div.entry > p::text').extract()
        news = ""
        for i in range(len(news_pera)):
            if(i > 0) :
                news += " "
            news += news_pera[i]
        yield {
            'headline': title,
            'body': news
        }