import json

with open('news_recent_all.json') as f:
    news = json.load(f)
#    print(news , type(news))
    
    for id in news:
        print(id , news[id]['title'])
    print(len(news.keys()))