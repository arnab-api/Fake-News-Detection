from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import TimeoutException

from Scraper import Scraper, Browser
import time
import json

count = 0
like_count = 0
comment_count = 0

def report(str):
    print('################## ' + str + ' ########################')

def get_news_id_from_url(url):
    if('story.php?story_fbid=' not in url):
        return -1
    arr = url.split('story.php?story_fbid=')
    arr = arr[1].split('&id=')
    return arr[0]


def GetBrowserAndLogIn():
    username = 'adhare.opsora.58'
    password = 'hola22hola'
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
    
    browser.driver.get(url)
    wait_cnt = 0
    while(True):
        try:
            html = browser.driver.page_source
            page_soup = BeautifulSoup(html , 'html.parser')
            
            comments_div = page_soup.find_all('div')
            comments_div = filter_comment_div(id , comments_div)
            
            comments = []
            global comment_count
            for cmt in comments_div:
        #        print(" ====> " , cmt.div.div.text ,"<=====")
                try:
                    cmt_text = cmt.div.div.text
                    if(len(cmt_text) == 0):
                        continue
                    comments.append(cmt_text)
                    comment_count += 1
                except Exception as e:
                    continue
            
            div = page_soup.find_all('div' , {'id': 'see_prev_'+id})
        #    print(len(div))
            if(len(div) != 0):
                url = "https://mbasic.facebook.com" + div[0].a['href']
                comments = comments + crawl_comments_for_the_post(id , url , browser)
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

#url = 'https://mbasic.facebook.com/story.php?story_fbid=653031741407285&id=184849354892195&refid=17&_ft_=top_level_post_id.653031741407285%3Atl_objid.653031741407285%3Athrowback_story_fbid.653031741407285%3Apage_id.184849354892195%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A653031741407285%2C%22publish_time%22%3A1388247209%2C%22story_name%22%3A%22EntShareCreationStory%22%2C%22object_fbtype%22%3A32%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntShareCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A184849354892195%2C%22actor_id%22%3A184849354892195%2C%22role%22%3A1%2C%22post_id%22%3A653031741407285%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.184849354892195%3A306061129499414%3A3%3A1357027200%3A1388563199%3A-3230210177284719249&__tn__=%2AW-R'
#id = get_news_id_from_url(url)
#comments = crawl_comments_for_the_post(id , url , browser)
#len(comments)
#print(comments)

''' ############# News ################## '''
def scrape_news(fb_moti_link , browser):
    browser.driver.get(fb_moti_link)
    wait_cnt = 0
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
            if(len(cc) == 0):
                return -1,-1
            cc = cc[0].a
            browser.driver.get(cc['href'])
            wait_cnt2 = 0
            time.sleep(2)
            while(True):
                try:
        #            time.sleep(5) # eita na dile zhamela kore 
                    ''' scrape news '''
                    html = browser.driver.page_source
                    page_soup = BeautifulSoup(html , 'html.parser')
                    
                    content = page_soup.find_all('div' , {'id': 'content'})
                    title = content[0].find_all('h2')[0].text    
                    entry = content[0].find_all('div' , {'class': 'entry'})
                    parr = entry[0].find_all('p')
                    
                    news = ""
                    for i in range(1 , len(parr) - 1):
                        news = news + " " + parr[i].text.strip()
                    
                    global count
                    count += 1
                    print(count ," =======> " , title)
        #            print(news)
                    return title , news
                except Exception as e:
                    print("page not loaded yet")
                    wait_cnt2 += 1
                    if(wait_cnt2 == 10):
                        wait_cnt2 = 0
                        print(" ------> refreshing")
                        browser.driver.get(cc['href'])
                    time.sleep(2)
                    continue
        except TimeoutException as e:
            print("loading...")
            wait_cnt += 1
            if(wait_cnt == 10):
                wait_cnt = 0
                print(" ------> refreshing")
                browser.driver.get(fb_moti_link)
            time.sleep(2)
            continue

#url2 = 'https://mbasic.facebook.com/story.php?story_fbid=856868737690250&id=184849354892195&refid=17&_ft_=top_level_post_id.856868737690250%3Atl_objid.856868737690250%3Athrowback_story_fbid.856868737690250%3Apage_id.184849354892195%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A856868737690250%2C%22publish_time%22%3A1421308477%2C%22story_name%22%3A%22EntShareCreationStory%22%2C%22object_fbtype%22%3A32%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntShareCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A184849354892195%2C%22actor_id%22%3A184849354892195%2C%22role%22%3A1%2C%22post_id%22%3A856868737690250%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.184849354892195%3A306061129499414%3A3%3A0%3A1533106799%3A-1771677856909800775&__tn__=%2AW-R'
#url = 'https://mbasic.facebook.com/story.php?story_fbid=744401152270343&id=184849354892195&refid=17&_ft_=top_level_post_id.744401152270343%3Atl_objid.744401152270343%3Athrowback_story_fbid.744401152270343%3Apage_id.184849354892195%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A744401152270343%2C%22publish_time%22%3A1404222017%2C%22story_name%22%3A%22EntShareCreationStory%22%2C%22object_fbtype%22%3A32%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntShareCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A184849354892195%2C%22actor_id%22%3A184849354892195%2C%22role%22%3A1%2C%22post_id%22%3A744401152270343%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.184849354892195%3A306061129499414%3A3%3A0%3A1533106799%3A3609503051877983563&__tn__=%2AW-R'
#url = 'https://mbasic.facebook.com/184849354892195/photos/a.443629492347512.97820.184849354892195/443629515680843/?type=3&refid=17&_ft_=top_level_post_id.443629515680843%3Atl_objid.443629515680843%3Athrowback_story_fbid.443629529014175%3Apage_id.184849354892195%3Aphoto_id.443629515680843%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A443629529014175%2C%22publish_time%22%3A1347924915%2C%22story_name%22%3A%22EntCoverPhotoEdgeStory%22%2C%22object_fbtype%22%3A22%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntCoverPhotoEdgeStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%7D%7D%3Athid.184849354892195%3A306061129499414%3A62%3A1325404800%3A1357027199%3A6561728436798253107&__tn__=%2AW-R'
#scrape_news(url , browser)


''' ############# Like ################## '''
def crawl_like_recursion(url, browser):
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
            likers = []
            global like_count
            for users in likers_div:
        #        print(users.a.text , users.a['href'])
        #        likers.append(users.a.text.strip())
                likers.append(users.a['href'])
                like_count += 1
            
                
            nxt = find_by_text(page_soup , 'a' , 'See more')
            if(len(nxt) == 0):
                return likers
            url = nxt[0]['href']
            add = crawl_like_recursion(url , browser)
            likers = likers + add
            
            return likers
        except TimeoutException as e:
            print("loading")
            if(wait_cnt == 10):
                wait_cnt = 0
                print(" ------> refreshing")
                browser.driver.get('https://mbasic.facebook.com' + url)
            time.sleep(2)
            continue

def crawl_likes_for_the_post(id,url, browser):
    browser.driver.get(url)
    wait_cnt = 0
    while(True):
        try:
            html = browser.driver.page_source
            page_soup = BeautifulSoup(html , 'html.parser')
            like_div = page_soup.find_all('div' , {'id': "sentence_"+id})
            likers = crawl_like_recursion(like_div[0].a['href'] , browser)
            
            return likers
        except TimeoutException as e:
            print("loading")
            if(wait_cnt == 10):
                wait_cnt = 0
                print(" ------> refreshing")
                browser.driver.get(url)
            time.sleep(2)
            continue

#url = 'https://mbasic.facebook.com/story.php?story_fbid=882811941762596&id=184849354892195&p=50&av=100024702038096&eav=AfYU1awJQGbISUWy9dWPkREGec6bA89xxbhPqR8b8OTE5PWIjXsEhCYLTt-hxsytsDI&refid=52&_ft_=top_level_post_id.882811941762596%3Atl_objid.882811941762596%3Athrowback_story_fbid.882811941762596%3Apage_id.184849354892195%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A882811941762596%2C%22publish_time%22%3A1425407588%2C%22story_name%22%3A%22EntShareCreationStory%22%2C%22object_fbtype%22%3A32%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntShareCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A184849354892195%2C%22actor_id%22%3A184849354892195%2C%22role%22%3A1%2C%22post_id%22%3A882811941762596%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.184849354892195'
#url = 'https://mbasic.facebook.com/story.php?story_fbid=203104779768018&id=184849354892195&refid=17&_ft_=top_level_post_id.203104779768018%3Atl_objid.203104779768018%3Athrowback_story_fbid.203104779768018%3Apage_id.184849354892195%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A203104779768018%2C%22publish_time%22%3A1321911562%2C%22story_name%22%3A%22EntShareCreationStory%22%2C%22object_fbtype%22%3A32%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntShareCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A184849354892195%2C%22actor_id%22%3A184849354892195%2C%22role%22%3A1%2C%22post_id%22%3A203104779768018%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.184849354892195%3A306061129499414%3A3%3A1293868800%3A1325404799%3A5548435578240779431&__tn__=%2AW-R'
#id = get_news_id_from_url(url)
#arr = crawl_likes_for_the_post(id, url, browser)
#print(len(arr))


''' ############# Crawl Everything ################## '''
def scrape_motikontho(id , url , browser , news_dict , comments_dict , likers_dict):
    
    try:
        global like_count , comment_count
        like_count = 0
        comment_count = 0
        title , news = scrape_news(url , browser)
        if(title == -1):
            return
#        likers = crawl_likes_for_the_post(id , url , browser)
#        comments = crawl_comments_for_the_post(id , url , browser)
        print("likes:" , like_count , " ---  Comments: ", comment_count)
        
    except TimeoutException as e:
        return
    
    news_dict[id] = {'id': id , 'title': title, 'news': news}
#    comments_dict[id] = comments
#    for user in likers:
##        print(user)
#        if(user not in likers_dict):
#            likers_dict[user] = []
#        likers_dict[user].append(id)


#url = 'https://mbasic.facebook.com/story.php?story_fbid=163841437091300&id=184849354892195&refid=17&_ft_=top_level_post_id.163841437091300%3Atl_objid.163841437091300%3Athrowback_story_fbid.163841437091300%3Apage_id.184849354892195%3Apage_insights.%7B%22184849354892195%22%3A%7B%22role%22%3A1%2C%22page_id%22%3A184849354892195%2C%22post_context%22%3A%7B%22story_fbid%22%3A163841437091300%2C%22publish_time%22%3A1351882315%2C%22story_name%22%3A%22EntShareCreationStory%22%2C%22object_fbtype%22%3A32%7D%2C%22actor_id%22%3A184849354892195%2C%22psn%22%3A%22EntShareCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A1%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22%3A184849354892195%2C%22actor_id%22%3A184849354892195%2C%22role%22%3A1%2C%22post_id%22%3A163841437091300%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.184849354892195%3A306061129499414%3A3%3A1325404800%3A1357027199%3A-5750231816080281932&__tn__=%2AW-R'
#id = get_news_id_from_url(url)
#scrape_motikontho(id , url , browser , news_dict , comments_dict , likers_dict)

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
                dvv = dv[i].find_all('div' , {'data-ft': '{"tn":"*W"}'})
                arr = dvv[0].find_all('a')
        #        print(len(arr))
                ''' Comment link is here '''
            #    arr[3]['href']
                url = 'https://mbasic.facebook.com' + arr[3]['href']
                id = get_news_id_from_url(url)
                if(id == -1):
                    continue
                scrape_motikontho(id , url , browser , news_dict , comments_dict , likers_dict)
            
            
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

''' go to motikontho '''
root_url = 'https://mbasic.facebook.com/%E0%A6%A6%E0%A7%88%E0%A6%A8%E0%A6%BF%E0%A6%95-%E0%A6%AE%E0%A6%A4%E0%A6%BF%E0%A6%95%E0%A6%A3%E0%A7%8D%E0%A6%A0-184849354892195/'
root_url13 = 'https://mbasic.facebook.com/profile.php?v=timeline&sectionLoadingID=m_timeline_loading_div_1388563199_1357027200_8_&timeend=1388563199&timestart=1357027200&tm=AQBN7PNJLjKDqtQc&id=184849354892195&refid=17'
root_url12 = 'https://mbasic.facebook.com/profile.php?v=timeline&timecutoff=1383426745&sectionLoadingID=m_timeline_loading_div_1357027199_1325404800_8_&timeend=1357027199&timestart=1325404800&tm=AQBLbjn93c-v6V4i&id=184849354892195&refid=17'
root_url11 = 'https://mbasic.facebook.com/profile.php?v=timeline&timecutoff=1383426745&sectionLoadingID=m_timeline_loading_div_1325404799_1293868800_8_&timeend=1325404799&timestart=1293868800&tm=AQD-8Y4UKreSlOvE&id=184849354892195&refid=17'
root_url_demo = 'https://mbasic.facebook.com/profile.php?sectionLoadingID=m_timeline_loading_div_1533106799_0_36_timeline_unit%3A1%3A00000000001383673072%3A04611686018427387904%3A09223372036854775512%3A04611686018427387904&unit_cursor=timeline_unit%3A1%3A00000000001383673072%3A04611686018427387904%3A09223372036854775512%3A04611686018427387904&timeend=1533106799&timestart=0&tm=AQBpvl4GKxzrOzta&id=184849354892195&refid=17'
browser = GetBrowserAndLogIn()

Scrape(root_url_demo , browser , news_dict , comments_dict , likers_dict)

print("Saving data")
with open('news_demo.json', 'w') as fp:
    json.dump(news_dict, fp)
with open('comments_demo.json', 'w') as fp:
    json.dump(comments_dict, fp)
with open('likers_demo.json', 'w') as fp:
    json.dump(likers_dict, fp)