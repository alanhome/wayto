# -*- coding: utf-8 -*-  
import web
import os
import json
import weibo
import urllib
from weibo import APIClient
import time
import hashlib
import sae

urls = (
    '/$', 'index',
	'/getpics$','get_pics',
	'/gettweets$','get_tweets',
	'/getviewsightsaccount$','get_viewsights_account'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)


def get_client():
	APP_KEY = '32434344444' # app key
	APP_SECRET = '699b0252d6c6fdsafdsab09858f49458c681' # app secret

	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET)
	access_token = "2.0fdsafdsafdsafd9F_7E"  #access token
	expires_in = 360000000000
	client.set_access_token(access_token, expires_in)
	return client
#location/pois/search/by_location.json

def get_location(client, query="颐和园"):
	try:
		locations = client.get.location__pois__search__by_location(q=query, category="110000",city="0010")
		lon = locations["pois"][0]["longitude"].encode("utf8")
		lat = locations["pois"][0]["latitude"].encode("utf8")
		print "search location sucess"
	except Exception:
		print "search location from query failed"
		lon = "116.2739"
		lat = "39.99957"
	return lon,lat


class index:        
    def GET(self):
		x = web.input().get('query', '')
		if x != '':
			return render.result(x)
		return render.index()

def base62_encode(num):
	alphabet  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if (num == 0):return alphabet[0]
	arr = []
	base = len(alphabet)
	while num:
		rem = num % base
		num = num / base
		arr.append(alphabet[rem])
	arr.reverse()
	return ''.join(arr)

def fill_tweet_template(jsonobj,client):
	divs = ''   
	template  = r'<a href="%s" target="_blank;"><div class= "row bub" name = "tweet" style="border-radius: 10px;border-width: 2px;margin-top:10px"><div class="span2" style="width:100px"><img src="%s" width="100px" height="100px" style="margin-top:5px"/><div style="text-align:center;">%s</div></div><div class="span4"><p style="font-family: 微软雅黑;font-size: 12px;margin-top:3px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</p></div></div></a>'
	# head_pic  username  text
	tweets_list = jsonobj["statuses"]
	for tweet in tweets_list:
		try:
			head_pic =  tweet["user"]["profile_image_url"].encode("utf8").replace("/50/","/180/")
			mid = client.statuses__querymid(id=str(tweet["mid"]), type="1")["mid"]
			userid =   str(tweet["user"]["id"])
			url = ("http://www.weibo.com/"+userid+"/"+mid).encode("utf8")
			username =  tweet["user"]["name"].encode("utf8")
			text = tweet["text"].encode("utf8")
			divs+= template%(url,head_pic,username,text)
		except Exception:
			continue
	return divs


class get_tweets:
	def GET(self):
		client = get_client()
		x = web.input().get('query', '颐和园')
		page = web.input().get('page','1')
		
		lon,lat = get_location(client, x)
		jsonobj = client.get.place__nearby_timeline(long=lon,lat= lat)

		divs =  fill_tweet_template(obj,client)
		return divs

class get_viewsights_account:
	def GET(self):
		divs = ''
		# username  location  description  head_pic  username   guanzhu  fensi  weibo
		template = r'<div class="row" style="background-color:white;height:160px; white;border-radius: 10px;margin-top:20px"><div class="span8"><div class="row" style="height:50px;"><div class="span6"><div class="row"><div class="span4"><div style="font-size:30px;float:left;line-height: 50px;"><B>%s</B></div>&nbsp;&nbsp;&nbsp;<i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star-empty" style="float:left;margin-top:17px"></i></div><div class="span2" style="line-height: 50px;"><i class="icon-thumbs-up" style="float:left;margin-top:17px"></i><div style="color:red;float:left;">43241</div><i class="icon-thumbs-down" style="float:left;margin-top:17px;margin-left:10px"></i><div style="color:green;float:left;">3241</div></div></div><div class="row" style="margin-left:3px">%s</div></div><div class="span2"><img src="/static/img/weather.png" /></div></div><div style="clear:both;"></div><div class="row" style="margin-left:3px;margin-top:3px">%s</div></div><div class="span4"><div class="row"><div class="span2" style="width:110px"><a href="%s" target="_blank;"><img src="%s" width="100px" height="100px" style="margin-top:10px"/></a></div><div class="span2"><div class="row" style="line-height:50px"><div style="float:left">%s</div><img style="float:left;margin-top:11px;margin-left:5px" src="/static/img/verified.png"/></div><div class="row"><div style="float:left;"><p>%s</p><p>关注</p></div><div style="float:left;margin-left:10px">	<p>%s</p><p>粉丝</p></div><div style="float:left;margin-left:10px"><p>%s</p><p>微博</p></div></div><div class="row"><img src="/static/img/focus.jpg" style="margin-top: 10px;" /></div></div></div></div></div>'
		x = web.input().get('query', '颐和园').encode("utf8")
		print x+"---------------aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		client = get_client()
		flag = 1
		try:
			user = client.get.users__show(screen_name=x)
			link =  ("http://www.weibo.com/u/"+str(user["id"])).encode("utf8")
			head_pic = user["profile_image_url"].replace("/50/","/180/").encode("utf8")
			username = user["name"].encode("utf8")
			description = user["description"].encode("utf8")
			followers_count = str(user["followers_count"]).encode("utf8")
			friends_count  = str(user["friends_count"]).encode("utf8")
			statuses_count = str(user["statuses_count"]).encode("utf8")
			location  = user["location"].encode("utf8")
		except Exception:
			flag = None
		
		if flag is not None:
			divs = template%(username,location, description, link,head_pic, username, friends_count,followers_count,statuses_count)
		else:
			divs = '<div>not found</div>'
		return divs

class  get_pics:
	def GET(self):
		divs = ''
		template = r'<div class="row" style="height:274px"><a href="%s" target="_blank;"><div name = "tweet" class="bub" style="border-radius: 10px;border-width: 2px;margin-top:10px;width:230px;height:274px;float:left;margin-left:10px;"><img src="%s" style="margin-left:15px;margin-top:30px;width:200px;height:200px;"/></div></a><a href="%s" target="_blank;"><div name = "tweet" class= "bub" style="border-radius: 10px;border-width: 2px;margin-top:10px;width:230px;height:274px;float:left;margin-left:10px;"><img src="%s" style="margin-left:15px;margin-top:30px;width:200px;height:200px;"/></div></a></div>'
		x = web.input().get('query', '颐和园')
		page = web.input().get('page','1')
		client = get_client()
		lon, lat = get_location(client,x)
		jsonobj = client.get.place__nearby__photos(long= lon,lat=lat, page = page)
		tweets_list = jsonobj["statuses"]
		l = len(tweets_list)
		for i in range(0,l,2):
			mid1 = client.statuses__querymid(id=str(tweets_list[i]["mid"]), type="1")["mid"]
			userid1 =   str(tweets_list[i]["user"]["id"])
			url1 = ("http://www.weibo.com/"+userid1+"/"+mid1).encode("utf8")
			mid2 = client.statuses__querymid(id=str(tweets_list[i+1]["mid"]), type="1")["mid"]
			userid2 =   str(tweets_list[i+1]["user"]["id"])
			url2 = ("http://www.weibo.com/"+userid2+"/"+mid2).encode("utf8")
			pic_url1 = tweets_list[i]["bmiddle_pic"].encode("utf8")
			pic_url2 = tweets_list[i+1]["bmiddle_pic"].encode("utf8")
			divs +=  template%(url1,pic_url1,url2, pic_url2)
		return divs


app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)			
	
if __name__ == "__main__":
    app.run()
