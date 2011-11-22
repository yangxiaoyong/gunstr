import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = range(10)
        self.render("tpl/demo.html", title="test_title", items=items)

app = tornado.web.Application([
    (r"/", MainHandler)
    ], xsrf_cookies=True)

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
