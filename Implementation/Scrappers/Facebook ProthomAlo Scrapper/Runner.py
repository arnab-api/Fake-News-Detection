from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import TimeoutException

from Scraper import Scraper, Browser
import time
import json

news_limit = 100000
like_limit = 2000
comment_limit = 100
count = 0
like_count = 0
comment_count = 0

def report(str):
    print('################## ' + str + ' ########################')

def save_data(news_dict , comments_dict , likers_dict):
    print("Saving data")
    with open('news_recent_all.json', 'w') as fp:
        json.dump(news_dict, fp)
    with open('comments_recent_all.json', 'w') as fp:
        json.dump(comments_dict, fp)
    with open('likers_recent_all.json', 'w') as fp:
        json.dump(likers_dict, fp)

def get_news_id_from_url(url):
    if('story.php?story_fbid=' not in url):
        return -1
    arr = url.split('story.php?story_fbid=')
    arr = arr[1].split('&id=')
    return arr[0]


def GetBrowserAndLogIn():
    username = 'osproshyo.sust@gmail.com'
    password = '49171123'
    report('Logging in for: ' + username)
    browser = Browser()
    browser.Login(username, password)
    try:
        okButton = browser.okButton()
        print(okButton)
        okButton.click()
    except Exception as e:
        print('Error is: ', e)
    
    report('Logged In')
    return browser

def find_by_text(page_soup , tag , text):
    elm_arr = page_soup.find_all(tag)
    ret = []
    for nx in elm_arr:
        if(nx.text == text):
            ret.append(nx)
    return ret

''' ############# Comment ################## '''
def check_div_id_for_comment(div_id):
    if(len(div_id) < 15):
        return False
    for i in range(len(div_id)):
        if(div_id[i] < '0' or div_id[i] > '9'):
            return False
    return True

def filter_comment_div(id , div_arr):
    comment_div_arr = []
    for div in div_arr:
        if(div.has_attr('id') == False):
            continue
        if(div['id'] == id):
            continue
        flag = check_div_id_for_comment(div['id'])
        if(flag == True):
            comment_div_arr.append(div)
    return comment_div_arr
        

def crawl_comments_for_the_post(id , url , browser):
    comments = []
    global comment_count , comment_limit
    while(True):
        browser.driver.get(url)
        wait_cnt = 0
        while(True):
            try:
                html = browser.driver.page_source
                page_soup = BeautifulSoup(html , 'html.parser')
                
                comments_div = page_soup.find_all('div')
                comments_div = filter_comment_div(id , comments_div)
                for cmt in comments_div:
            #        print(" ====> " , cmt.div.div.text ,"<=====")
                    try:
                        cmt_text = cmt.div.div.text
                        if(len(cmt_text) == 0):
                            continue
                        comments.append(cmt_text)
                        comment_count += 1
                        if(comment_count > comment_limit):
                            return comments
                    except Exception as e:
                        continue
                
                div = page_soup.find_all('div' , {'id': 'see_next_'+id})
            #    print(len(div))
                if(len(div) != 0):
                    url = "https://mbasic.facebook.com" + div[0].a['href']
                    break
                return comments
            
            except TimeoutException as e:
                    print("loading...")
                    wait_cnt += 1
                    if(wait_cnt == 10):
                        wait_cnt = 0
                        print(" ------> refreshing")
                        browser.driver.get(url)
                    time.sleep(2)
                    continue
    return comments

# url = 'https://mbasic.facebook.com/story.php?story_fbid=2147285971971144&id=163059227060505&refid=17&_ft_=top_level_post_id.2147285971971144%3Atl_objid.2147285971971144%3Athrowback_story_fbid.2147285971971144%3Apage_id.163059227060505%3Apage_insights.%7B%22163059227060505%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A163059227060505%2C%22post_context%22%3A%7B%22story_fbid%22%3A2147285971971144%2C%22publish_time%22%3A1532774226%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22object_fbtype%22%3A266%7D%2C%22actor_id%22%3A163059227060505%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A163059227060505%2C%22actor_id%22%3A163059227060505%2C%22role%22%3A1%2C%22post_id%22%3A2147285971971144%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.163059227060505%3A306061129499414%3A2%3A0%3A1533106799%3A5252313976052576853&__tn__=%2AW-R'
# browser = GetBrowserAndLogIn()
# id = get_news_id_from_url(url)
# comments = crawl_comments_for_the_post(id , url , browser)
# print(len(comments))

''' ############# News ################## '''
def scrape_news(fb_alo_link , browser):
    browser.driver.get(fb_alo_link)
    wait_cnt = 0
    refresh_count = 0
    while(True):
        try:
            html = browser.driver.page_source
            page_soup = BeautifulSoup(html , 'html.parser')
            '''news_link'''
        #    cc = page_soup.find_all('a' , {'class': 'bm bn'})
        #    if(len(cc) == 0):0
        #        cc = page_soup.find_all('a' , {'class': 'bp bq'})
        #    if(len(cc) == 0):
        #        cc = page_soup.find_all('a' , {'class': 'bk bl'})
            cc = page_soup.find_all('div' , {'data-ft': '{"tn":"H"}'})
            try:
                cc = cc[0].a
                news_url = cc['href']
                browser.driver.get(news_url)
            except Exception as e:
                return -1,-1
            
            wait_cnt2 = 0
            time.sleep(2)
            while(True):
                try:
        #            time.sleep(5) # eita na dile zhamela kore 
                    ''' scrape news '''
#                    src = 'http://www.prothomalo.com/international/article/1538631/%E0%A6%87%E0%A6%AE%E0%A6%B0%E0%A6%BE%E0%A6%A8%E0%A7%87%E0%A6%B0-%E0%A6%9C%E0%A7%80%E0%A6%AC%E0%A6%A8%E0%A7%87%E0%A6%B0-%E0%A6%B8%E0%A6%AC%E0%A6%9A%E0%A7%87%E0%A7%9F%E0%A7%87-%E0%A6%AC%E0%A7%9C-%E0%A6%AD%E0%A7%81%E0%A6%B2'
#                    browser.driver.get(src)
                    html = browser.driver.page_source
                    page_soup = BeautifulSoup(html , 'html.parser')
                    
                    title = page_soup.find_all('h1' , {'class': 'title'})
                    title = title[0].text
                    
                    parr = page_soup.find_all('p')
                    news = ""
                    for i in range(0 , len(parr) - 2):
                        news = news + " " + parr[i].text.strip()
                    
                    global count
                    count += 1
                    print(count ," =======> " , title)
#                    print(news)
                    return title , news
                except Exception as e:
                    print("page not loaded yet or Problem scraping news...")
                    wait_cnt2 += 1
                    if(wait_cnt2 == 10):
                        wait_cnt2 = 0
                        print(" ------> refreshing" , refresh_count+1)
                        refresh_count += 1
                        if(refresh_count == 5):
                            return -1,-1
                        browser.driver.get(cc['href'])
                    time.sleep(2)
                    continue
        except TimeoutException as e:
            print("loading...")
            wait_cnt += 1
            if(wait_cnt == 10):
                wait_cnt = 0
                print(" ------> refreshing")
                browser.driver.get(fb_alo_link)
            time.sleep(2)
            continue

#url = 'https://mbasic.facebook.com/story.php?story_fbid=2139003336132741&id=163059227060505&refid=17&_ft_=top_level_post_id.2139003336132741%3Atl_objid.2139003336132741%3Athrowback_story_fbid.2139003336132741%3Apage_id.163059227060505%3Apage_insights.%7B%22163059227060505%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A163059227060505%2C%22post_context%22%3A%7B%22story_fbid%22%3A2139003336132741%2C%22publish_time%22%3A1532372340%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22object_fbtype%22%3A266%7D%2C%22actor_id%22%3A163059227060505%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A163059227060505%2C%22actor_id%22%3A163059227060505%2C%22role%22%3A1%2C%22post_id%22%3A2139003336132741%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.163059227060505%3A306061129499414%3A2%3A0%3A1533106799%3A2885776035279950855&__tn__=%2AW-R'
#scrape_news(url , browser)


''' ############# Like ################## '''
def crawl_like_recursion(url, browser):
    likers = []
    global like_count , like_limit
    while(True):
        browser.driver.get('https://mbasic.facebook.com' + url)
        wait_cnt = 0
        while(True):
            try:
                html = browser.driver.page_source
                page_soup = BeautifulSoup(html , 'html.parser')
                likers_div = page_soup.find_all('h3' , {'class': 'bi'})
                if(len(likers_div) == 0):
                    likers_div = page_soup.find_all('h3' , {'class': 'bj'})
            #    print(len(likers_div))
                for users in likers_div:
            #        print(users.a.text , users.a['href'])
            #        likers.append(users.a.text.strip())
                    likers.append(users.a['href'])
                    like_count += 1
                    if(like_count > like_limit):
                        return likers
                    
                nxt = find_by_text(page_soup , 'a' , 'See more')
                if(len(nxt) == 0):
                    return likers
                url = nxt[0]['href']
                break
                
                # return likers
            except TimeoutException as e:
                print("loading")
                if(wait_cnt == 10):
                    wait_cnt = 0
                    print(" ------> refreshing")
                    browser.driver.get('https://mbasic.facebook.com' + url)
                time.sleep(2)
                continue
    return likers

def crawl_likes_for_the_post(id,url, browser):
    browser.driver.get(url)
    wait_cnt = 0
    while(True):
        try:
            html = browser.driver.page_source
            page_soup = BeautifulSoup(html , 'html.parser')
            like_div = page_soup.find_all('div' , {'id': "sentence_"+id})
            if(len(like_div) > 0):
                likers = crawl_like_recursion(like_div[0].a['href'] , browser)
                return likers
            return -1
        except TimeoutException as e:
            print("loading")
            if(wait_cnt == 10):
                wait_cnt = 0
                print(" ------> refreshing")
                browser.driver.get(url)
            time.sleep(2)
            continue

# url = 'https://mbasic.facebook.com/story.php?story_fbid=2150935638272844&id=163059227060505&refid=17&_ft_=top_level_post_id.2150935638272844%3Atl_objid.2150935638272844%3Athrowback_story_fbid.2150935638272844%3Apage_id.163059227060505%3Apage_insights.%7B%22163059227060505%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A163059227060505%2C%22post_context%22%3A%7B%22story_fbid%22%3A2150935638272844%2C%22publish_time%22%3A1532942423%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22object_fbtype%22%3A266%7D%2C%22actor_id%22%3A163059227060505%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A163059227060505%2C%22actor_id%22%3A163059227060505%2C%22role%22%3A1%2C%22post_id%22%3A2150935638272844%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.163059227060505%3A306061129499414%3A2%3A0%3A1533106799%3A7874634797451458743&__tn__=%2AW-R'
# id = get_news_id_from_url(url)
# browser = GetBrowserAndLogIn()
# arr = crawl_likes_for_the_post(id, url, browser)
# print(len(arr))


''' ############# Crawl Everything ################## '''
def scrape_motikontho(id , url , browser , news_dict , comments_dict , likers_dict):
    
    try:
        global like_count , comment_count
        like_count = 0
        comment_count = 0
        title , news = scrape_news(url , browser)
        if(title == -1):
            return
        # title = "Title"
        # news = "khobor"

        likers = crawl_likes_for_the_post(id , url , browser)
        if(likers == -1):
            return
        comments = crawl_comments_for_the_post(id , url , browser)
        print("id:" , id , ' --- likes:' , like_count , " --- Comments: ", comment_count)
        
    except Exception as e:
        return
    
    news_dict[id] = {'id': id , 'title': title, 'news': news}
    
    comments_dict[id] = comments
    for user in likers:
#        print(user)
        if(user not in likers_dict):
            likers_dict[user] = []
        likers_dict[user].append(id)
    
    global count
    if(count % 10 == 0):
        save_data(news_dict , comments_dict , likers_dict)

# browser = GetBrowserAndLogIn()
# news_dict = {}
# comments_dict = {}
# likers_dict = {}
# url = 'https://mbasic.facebook.com/story.php?story_fbid=2150935638272844&id=163059227060505'
# id = get_news_id_from_url(url)
# scrape_motikontho(id , url , browser , news_dict , comments_dict , likers_dict)

def Scrape(root_url , browser , news_dict , comments_dict , likers_dict):
    browser.driver.get(root_url)
    wait_cnt = 0
    while(True):
        try:
            html = browser.driver.page_source
            page_soup = soup(html , 'html.parser')
            dv = page_soup.find_all('div' , {'role': 'article'})
        #    print(len(dv))
            
            for i in range(len(dv)):
        #        dvv = dv[i].find_all('div' , {'class': 'ew'})
        #        if(len(dvv) == 0):
        #            dvv = dv[i].find_all('div' , {'class': 'eu'})
                try:
                    dvv = dv[i].find_all('div' , {'data-ft': '{"tn":"*W"}'})
                    arr = dvv[0].find_all('a')
            #        print(len(arr))
                    ''' Comment link is here '''
                #    arr[3]['href']
                    url = 'https://mbasic.facebook.com' + arr[3]['href']
                except Exception as e:
                    continue
                id = get_news_id_from_url(url)
                if(id == -1):
                    continue
                scrape_motikontho(id , url , browser , news_dict , comments_dict , likers_dict)
            
            global count , news_limit
            if(count > news_limit):
                print("Enough Real News Scraped ...... EXITING")
                return
            
            nxnx_div = page_soup.find_all('div' , {'class': 'i'})
            len(nxnx_div)
            next_div = None
            for dv in nxnx_div:
                if(dv.text == 'Show more'):
                    next_div = dv
            if(next_div != None):
                next_url = 'https://mbasic.facebook.com' + next_div.a['href']
                Scrape(next_url , browser , news_dict , comments_dict , likers_dict)
            print("Exiting")
            return
            
        except TimeoutException as e:
            print("loading")
            if(wait_cnt == 10):
                wait_cnt = 0
                print(" ------> refreshing")
                browser.driver.get(root_url)
            time.sleep(2)
            continue
        
news_dict = {}
comments_dict = {}
likers_dict = {}

# print(len(news_dict.keys()))

''' go to motikontho '''
browser = GetBrowserAndLogIn()

root_url = 'https://mbasic.facebook.com/DailyProthomAlo/'
root_url_2018 = 'https://mbasic.facebook.com/DailyProthomAlo?v=timeline&timecutoff=1531726215&sectionLoadingID=m_timeline_loading_div_1546329599_1514793600_8_&timeend=1546329599&timestart=1514793600&tm=AQAKB_qyjOYPHCbW&refid=17'
root_url_2011 = 'https://mbasic.facebook.com/DailyProthomAlo?v=timeline&timecutoff=1531678589&sectionLoadingID=m_timeline_loading_div_1325404799_1293868800_8_&timeend=1325404799&timestart=1293868800&tm=AQDsRdJlA5eJ0JPb&refid=17'
Scrape(root_url , browser , news_dict , comments_dict , likers_dict)

save_data(news_dict , comments_dict , likers_dict)