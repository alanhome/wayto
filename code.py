# -*- coding: utf-8 -*-  
import web
import os
import json
import weibo
from weibo import APIClient

urls = (
    '/$', 'index',
	'/getpics$','get_pics',
	'/testp$', 'testp',
	'/gettweets','get_tweets',
	
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

class index:        
    def GET(self):
		x = web.input().get('query', '')
		if x != '':
			return render.result()
		return render.index()

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
		client = get_client()
		jsonobj = client.get.place__poi_timeline(poiid="B2094654D16CABFE419E")
		divs = fill_tweet_template(jsonobj)
		return divs

class  get_pics:
	def GET(self):
		client = get_client()
		jsonobj = client.get.place__pois__photos(poiid="B2094654D16CABFE419E")
		return jsonobj
	
if __name__ == "__main__":
    app.run()
