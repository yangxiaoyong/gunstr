import tornado.web
import tornado.ioloop

from tornado import httpclient

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = httpclient.AsyncHTTPClient()
        http.fetch("http://g.cn", self._on_download)

    def _on_download(self, response):
        self.write("Downloaded!" + str(response))
        self.finish()


app = tornado.web.Application([
    ("/", AsyncHandler)
    ])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
