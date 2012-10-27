import web
import os

urls = (
    '/$', 'index'
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

if __name__ == "__main__":
    app.run()
