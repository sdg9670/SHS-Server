import requests

def crawl(keyword):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="+keyword
    data = requests.get(url)
    print(data.status_code,url)
    return data.content
