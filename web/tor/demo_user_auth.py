import tornado.web
import tornado.ioloop
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, %s" % name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                'Name: <input type="text" name="name">'
                '<input type="submit" value="Sign in">'
                '</form></body></html>'
                )

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

settings = {
        "cookie_secret": "abc",
        "login_url": "/login",
        "debug": True,
        }

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler)
    ], **settings)

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

