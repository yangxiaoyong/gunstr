import tornado.web
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("mycookie"):
            self.set_cookie("mycookie", "ten_yuan")
            self.write("Your cookie not set yet")
        else:
            self.write("Your cookie already set")

class SMainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("uc"):
            self.set_secure_cookie("uc", "1")
            self.write("Your cookie not set yet")
        else:
            self.write("Your cookie already set: %s" % self.get_cookie("uc"))

app = tornado.web.Application([
    ("/", SMainHandler),
    ], cookie_secret="cookie_secret")

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
