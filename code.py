# -*- coding: utf-8 -*-  
import web
import os
import json
import weibo


urls = (
    '/$', 'index',
	'/getpic$','getpic',
	'/testp$', 'testp', 
	
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
app = web.application(urls, globals())

class index:        
    def GET(self):
		x = web.input().get('query', '')
		if x != '':
			return render.result()
		return render.index()

class testp:
	def GET(self):
		str = '{"statuses": [{"created_at": "Sat Oct 27 19:57:27 +0800 2012","id": "3505832429665645","mid": "3505832429665645","idstr": "3505832429665645","text": "RUCers Style http://t.cn/zl1fvbh","source": "<a href=\"http://m.weibo.com/web/cellphone.phpandroid\" rel=\"nofollow\">Android</a>","favorited": false,"truncated": false,"in_reply_to_status_id": "","in_reply_to_user_id": "","in_reply_to_screen_name": "","geo": {"type": "Point","coordinates": [39.970817,116.316032]},"user": {"id": "1647047964","idstr": "1647047964","screen_name": "angel9k5","name": "angel9k5","province": "11","city": "8","location": "","description": "","url": "","profile_image_url": "http://tp1.sinaimg.cn/1647047964/50/5600912871/0","profile_url": "u/1647047964","domain": "","weihao": "","gender": "f","followers_count": 120,"friends_count": 191,"statuses_count": 465,"favourites_count": 30,"created_at": "Sun Oct 11 17:25:05 +0800 2009","following": false,"allow_all_act_msg": false,"geo_enabled": true,"verified": false,"verified_type": -1,"remark": "","allow_all_comment": true,"avatar_large": "http://tp1.sinaimg.cn/1647047964/180/5600912871/0","verified_reason": "","follow_me": false,"online_status": 0,"bi_followers_count": 56,"lang": "zh-cn","star": 0,"level": 1,"type": 1,"ulevel": 0,"badge": {"kuainv": {"level": 0},"uc_domain": 0,"enterprise": 0,"anniversary": 0}},"reposts_count": 0,"comments_count": 0,"attitudes_count": 0,"mlevel": 0,"visible": {"type": 0,"list_id": 0},"distance": 1700}],"total_number": 6131,"states": [{"id": "3505832429665645","state": 0}]}'
		return str




if __name__ == "__main__":
    app.run()
