from flask import Flask, render_template, request
from pyfcm import FCMNotification
import json

import databaseManager

db = databaseManager.DatabaseManager('localhost','root','!Dasom0129','shs')
push_service = FCMNotification(api_key="AAAAXE7sxxA:APA91bGJVD6TxWf_9WBZS97vToJ18SG-OnslG8g-crwm1WjJxPVa9gBvPFm3C4ma0lpHuOZuLOepeOPftXA4DmBQjcsejFFKjt2rFarqpdk8zNm2oay-JCLpu5N_bAWezdSKYGUP8RD1")

import requests as rq
app = Flask(__name__)

from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAAXE7sxxA:APA91bGJVD6TxWf_9WBZS97vToJ18SG-OnslG8g-crwm1WjJxPVa9gBvPFm3C4ma0lpHuOZuLOepeOPftXA4DmBQjcsejFFKjt2rFarqpdk8zNm2oay-JCLpu5N_bAWezdSKYGUP8RD1")

def sendFCM_Dong():
    result = push_service.notify_multiple_devices(registration_ids=["e1UhCjS8Wcw:APA91bE5hm8-9wJ7JuJchscz9qct5SS6pIbyqtjA-foRT49A56soZb7DDYL5uNc9wKtGVgQxhXwIwOuVcSYa4zdd6jxTd1RbP0T44Q5s7k1fGzeUKLOYb9LXycuwYjphGzDwofYXe1A5"], message_title="zz", message_body="kk")
    print(result)

def sendFCM():
    result = push_service.notify_single_device(registration_id="e1UhCjS8Wcw:APA91bE5hm8-9wJ7JuJchscz9qct5SS6pIbyqtjA-foRT49A56soZb7DDYL5uNc9wKtGVgQxhXwIwOuVcSYa4zdd6jxTd1RbP0T44Q5s7k1fGzeUKLOYb9LXycuwYjphGzDwofYXe1A5", message_title="zz", message_body="ll")
    print(result)

if __name__ == '__main__':
    fcm()
    #app.run(debug=True, host='0.0.0.0')