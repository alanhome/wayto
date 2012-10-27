# -*- coding: utf-8 -*-  
import web
import os
import json
import weibo
import urllib
from weibo import APIClient
import time
import hashlib

urls = (
    '/$', 'index',
	'/getpics$','get_pics',
	'/gettweets$','get_tweets',
	'/getviewsightsaccount$','get_viewsights_account'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
app = web.application(urls, globals())

def get_client():
	APP_KEY = '1063723722' # app key
	APP_SECRET = 'a4615d9d75ac60761fd07c981561b4a7' # app secret
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET)
	access_token = "2.00fzbvLCOIRzJB87e710d44be2CfhD"
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

def get_tweets1(query = "颐和园"):
	url = 'http://mblog.city.sina.com.cn/index.php?app=api&mod=Interface&act=get_search_statuses'
	tm = int(time.time())
	key = "SDAFA@#$@#$*^%*&DDDMdsf"
	token = hashlib.md5(str(tm)+key).hexdigest()
	access_token = "123"
	url += "&token="+token
	url += "&time="+str(tm)
	url += "&q="+query.encode("utf8")
	url += "&access_token="+access_token
	ans = urllib.urlopen(url).read()
	return ans

def fill_tweet_template(jsonobj):
	divs = ''   
	template  = r'<div class= "row" name = "tweet" style="background-color: white;border-radius: 10px;border-width: 2px;margin-top:10px"><div class="span2" style="width:100px"><img src="%s" width="100px" height="100px" style="margin-top:5px"/><div style="text-align:center;">%s</div></div><div class="span4"><p style="font-family: 微软雅黑;font-size: 12px;margin-top:3px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</p></div></div>'   # head_pic  username  text
	tweets_list = jsonobj["statuses"]
	for tweet in tweets_list:
		try:
			head_pic =  tweet["user"]["profile_image_url"].encode("utf8").replace("/50/","/180/")
			username =  tweet["user"]["name"].encode("utf8")
			text = tweet["text"].encode("utf8")
			divs+= template%(head_pic,username,text)
		except Exception:
			continue
	return divs


class get_tweets:
	def GET(self):
		print "fuck here"
		client = get_client()
		x = web.input().get('query', '颐和园')
		ans = get_tweets1(x)
		obj = weibo.json.loads(ans)
		obj =  obj["result"]
		#lon,lat = get_location(client, x)
		#jsonobj = client.get.place__nearby_timeline(long=lon,lat= lat)
		#divs = fill_tweet_template(jsonobj)
		divs =  fill_tweet_template(obj)
		return divs

class get_viewsights_account:
	def GET(self):
		divs = ''
		# username  location  description  url  username   guanzhu  fensi  weibo
		template = r'<div class="row" style="background-color:white;height:160px; white;border-radius: 10px;margin-top:20px"><div class="span8"><div class="row" style="height:50px;"><div class="span6"><div class="row"><div class="span3"><div style="font-size:30px;float:left;line-height: 50px;"><B>%s</B></div>&nbsp;&nbsp;&nbsp;<i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star" style="float:left;margin-top:17px"></i><i class="icon-star-empty" style="float:left;margin-top:17px"></i></div><div class="span3" style="line-height: 50px;"><i class="icon-thumbs-up" style="float:left;margin-top:17px"></i><div style="color:red;float:left;">43241</div><i class="icon-thumbs-down" style="float:left;margin-top:17px;margin-left:10px"></i><div style="color:green;float:left;">3241</div></div></div><div class="row" style="margin-left:3px">%s</div></div><div class="span2"><img src="/static/img/weather.png" /></div></div><div style="clear:both;"></div><div class="row" style="margin-left:3px;margin-top:3px">%s</div></div><div class="span4"><div class="row"><div class="span2" style="width:110px"><img src="%s" width="100px" height="100px" style="margin-top:10px"/></div><div class="span2"><div class="row" style="line-height:50px"><div style="float:left">%s</div><img style="float:left;margin-top:11px;margin-left:5px" src="/static/img/verified.png"/></div><div class="row">%s&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;%s</div><div class="row">关注&nbsp;&nbsp;&nbsp;粉丝&nbsp;&nbsp;&nbsp;微博</div><div class="row"><img src="/static/img/focus.jpg" style="margin-top: 10px;" /></div></div></div></div></div>'
		x = web.input().get('query', '颐和园')
		print x+"---------------aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		client = get_client()
		flag = 1
		try:
			user = client.get.users__show(screen_name=x)
			head_pic = user["profile_image_url"].encode("utf8").replace("/50/","/180/")
			username = user["name"].encode("utf8")
			description = user["description"].encode("utf8")
			followers_count = str(user["followers_count"])
			friends_count  = str(user["friends_count"])
			statuses_count = str(user["statuses_count"])
			location  = user["location"].encode("utf8")
		except Exception:
			flag = None
		if flag is not None:
			divs = template%(username,location, description, head_pic, username, friends_count,followers_count,statuses_count)
		else:
			divs = '<div>not found</div>'
		return divs

class  get_pics:
	def GET(self):
		divs = ''
		template = r'<div class="row" style="height:230px"><div name = "tweet" style="background-color: white;border-radius: 10px;border-width: 2px;margin-top:10px;width:230px;height:230px;float:left;margin-left:10px;"><img src="%s" style="margin-left:15px;margin-top:15px;width:200px;height:200px;"/></div><div name = "tweet" style="background-color: white;border-radius: 10px;border-width: 2px;margin-top:10px;width:230px;height:230px;float:left;margin-left:10px;"><img src="%s" style="margin-left:15px;margin-top:15px;width:200px;height:200px;"/></div></div>'
		x = web.input().get('query', '颐和园')
		client = get_client()
		lon, lat = get_location(client,x)
		jsonobj = client.get.place__nearby__photos(long= lon,lat=lat)
		tweets_list = jsonobj["statuses"]
		l = len(tweets_list)
		for i in range(0,l,2):
			pic_url1 = tweets_list[i]["bmiddle_pic"].encode("utf8")
			pic_url2 = tweets_list[i+1]["bmiddle_pic"].encode("utf8")
			divs +=  template%(pic_url1, pic_url2)
		return divs
			
	
if __name__ == "__main__":
    app.run()
