from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), weather['wind']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_chuanyi():
  url = "http://d1.weather.com.cn/zs_index/101110200.html?_=1661788197500"
  head ={}
  params= {}
  params={'enc':'utf-8'}
  head = {'Referer':'http://www.weather.com.cn/','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
  res = requests.get(url,headers=head)
  res.encoding = res.apparent_encoding
  a = res.text[17:-11]
  data=eval(a)
  yf = data['ct_des_s']
  return yf

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_gupiao():
    gpurl = "http://hq.sinajs.cn/list=gb_tsla"
    head = {}
    head = {'referer': "https://finance.sina.com.cn"}
    # print(head)
    gprequest = requests.get(gpurl, headers=head).text
    data = gprequest[14:-3].replace("=", ",").split(',')
    Price = data[2]
    return Price


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, wind= get_weather()

data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"chuanyi":{"value":get_chuanyi()},"gujia":{"value":get_gupiao()},"birthday_left":{"value":get_birthday()},"wind":{"value":wind} ,"words":{"value":get_words() ,"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
