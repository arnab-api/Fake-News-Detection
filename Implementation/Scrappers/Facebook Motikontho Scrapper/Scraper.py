import random
import time

import re
from bs4 import BeautifulSoup
from selenium import webdriver
import json


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

    # self.driver = webdriver.PhantomJS(r'pjs.exe')

    def Login(self, usr, pword):
        self.driver.get("https://mbasic.facebook.com")
        time.sleep(random.randrange(2, 5))
        self.driver.find_element_by_name('email').send_keys(usr)
        self.driver.find_element_by_name('pass').send_keys(pword)
        self.driver.find_element_by_name('pass').send_keys('\n')

    def goTo(self, link):
        self.driver.get(link)

    def getSource(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def close(self):
        self.driver.close()

    def okButton(self):
        return self.driver.find_element_by_css_selector("input[type='submit']")

    def getFriendsPage(self):
        ret = [
            link for link in self.driver.find_elements_by_link_text('See more friends')]
        for l in ret:
            print(l)
        return ret

    def photoCount(self, url):
        # self.driver.get(url + '/photos')
        try:
            if url.find('profile.php') != -1:
                link = url
                self.driver.get(link)
                time.sleep(1)
                self.driver.find_element_by_link_text('Photos').click()
            else:
                link = url + '/photos'
                self.driver.get(link)
        except Exception as e:
            return 0
        
        all = self.driver.find_elements_by_link_text('See All')
        # print('Photos Links -------> ',all)
        goto = None
        if (len(all) == 1):
            goto = all[0].click()
        elif (len(all) == 2):
            goto = all[1].click()
        elif (len(all) == 3):
            goto = all[1].click()
        else:
            return 0
        ret = 0
        while True:
            ret += 1
            try:
                goto = self.driver.find_element_by_link_text('See more photos')
            except Exception as e:
                break
            time.sleep(random.randrange(2, 4))
            goto.click()
        return ret * 12

    def getAllYear(self):
        div_section = self.driver.find_element_by_id('structured_composer_async_container')
        years = div_section.find_elements_by_xpath(".//*[@class='h']/a")
        links = []
        for year in years:
            print(year.text)
            links += [year.get_attribute('href')]
        return links

    def postDigger(self, url):

        self.goTo(url)
        taggedIn = 0
        allYear = self.getAllYear()[1:]
        totalPost = 0
        scraper = Scraper()
        for year in allYear:
            html = self.getSource(year)  
            while True:
                html = self.driver.page_source
                totalPost += 5
                scraper.setHtml(html)
                taggedIn += len(scraper.getElementFromText('is with'))
                if totalPost>=100:
                    break
                time.sleep(random.randrange(1,3))
                try:
                    page = self.driver.find_element_by_link_text('Show more')
                    page.click()
                except Exception as e:
                    break
                if page is None:
                    break
            if totalPost>=50:
                break
            time.sleep(random.randrange(1,2))

        return taggedIn, totalPost


class Scraper():

    def __init__(self):
        print("Hello I'm Scraper()")
        self.host = 'https://mbasic.facebook.com'

    def setHtml(self, html):
        self.bs = BeautifulSoup(html, 'html.parser')

    def getNavLinks(self):
        retVal = []
        links = self.bs.find_all('div', {'class': 'h'})
        for link in links:
            retVal.append((link.a.text, self.host + link.a['href']))
        return retVal

    def scrape(self):
        div = self.bs.find(
            'div', {'id': 'structured_composer_async_container'})
        divs = div.find_all('div', {'role': 'article'})

        retVal = []
        for d in divs:
            tmp = d.find_all('div')
            if len(tmp) >= 3:
                post = tmp[2].text
                retVal.append(post)
        return retVal

    def getElementFromText(self, text):
        return self.bs.findAll(text=re.compile(text))

    def extractId(self):
        ids = []
        for link in self.bs.findAll('td', {'class': 'v s'}):
            # print("test:---->  ", link)
            try:
                a = link.a['href'].find('?fref')
                b = link.a['href'].find('&fref')
                c = link.a['href']
                if a is not -1:
                    c = c[0:a]
                if b is not -1:
                    c = c[0:b]
                ids += [
                    [
                        c,
                        link.a.text
                    ]
                ]
            except Exception as e:
                print(e)
                print("Exception for friend : ", c)
        return ids

    def getData(self, name):
        ret = {'name': name}
        try:
            about = self.bs.find('div', {'id': 'bio'}).div.findAll(
                'div', recursive=False)[1].div.text
            ret['about'] = about
        except Exception as e:
            pass

        try:
            all_edu = self.bs.find('div', {'id': 'education'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                              recursive=False)
            edu = []
            for e in all_edu:
                edu += [{
                    'institution': e.div.div.div.div.span.text,
                    'type': e.div.findAll('div', recursive=False)[0].findAll('div', recursive=False)[1].text
                }]
            ret['education'] = edu
        except Exception as e:
            pass

        try:
            all = self.bs.find('div', {'id': 'living'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                       recursive=False)
            data = []
            for d_ in all:
                data += [{
                    d_.div.findAll('td')[0].text: d_.div.findAll('td')[1].text
                }]
            ret['living'] = data
        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'contact-info'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                             recursive=False)
            data = []
            for d_ in all:
                data += [{
                    d_.table.findAll('td')[0].text: d_.table.findAll('td')[1].text
                }]
            ret['contact-info'] = data
        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'family'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                       recursive=False)
            data = []
            for d_ in all:
                data += [{
                    d_.findAll('h3')[1].text: d_.findAll('h3')[0].text
                }]
            ret['family'] = data
        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'work'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                     recursive=False)
            data = []
            for d_ in all:
                p = {}
                i = 0
                for dd in d_.div.findAll('div', recursive=True):
                    p[str(i)] = dd.text
                    i += 1

                # data += [
                #     { random.choice('abc') : dd.text for dd in d_.div.findAll('div', recursive=False) }
                # ]
            ret['work'] = p

        except Exception as e:
            # print(e)
            pass
        try:
            all = self.bs.find('div', {'id': 'basic-info'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                           recursive=False)
            data = []
            for d_ in all:
                data += [
                    {d_.table.findAll('td')[0].text: d_.table.findAll('td')[
                        1].text}
                ]
            ret['basic-info'] = data

        except Exception as e:
            pass
        try:
            all = self.bs.find('div', {'id': 'nicknames'}).div.findAll('div', recursive=False)[1].findAll('div',
                                                                                                          recursive=False)
            data = []
            for d_ in all:
                data += [
                    d_.table.findAll('td')[1].text
                ]
            ret['nicknames'] = data
        except Exception as e:
            pass

        return ret
