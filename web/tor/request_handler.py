import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('You requested to the main page'
                '<html><body><form action="/" method="post" enctype="multipart/form-data">'
                '<input type="text" name="message"><br />'
                '<br />'
                '<input type="file" name="somefile" size=40>'
                '<input type="submit" value="Submit">'
                '</form></body></html>'
                )

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message") +
                "Http Headers: " + str(self.request.headers)
                )

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.user_is_logged_in():
            raise tornado.web.HTTPError(403)

    def user_is_logged_in(self):
        return False

class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story " + story_id)

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/admin", AdminHandler),
        (r"/story/([0-9]+)", StoryHandler),
    ])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

