#encoding:utf8

#TODO:
# 1. 写出上传的WEB表单页面
# 2. 处理上传表单
# 3. 转存上传的文件
# 4. 用户认真

import os.path

import tornado.ioloop
import tornado.web

UPLOAD_DIR = '/tmp'

class FileUploadHandler(tornado.web.RequestHandler):
    ''' 文件上传处理 '''

    def post(self):
        for key in self.request.files.iterkeys():
            fileobj = self.request.files[key][0]
            filename = fileobj['filename']

            self.savefile(os.path.join(UPLOAD_DIR, filename),
                          fileobj['body'])

        self.write('Uploaded successful!')
        self.finish()

    def savefile(self, path, content):
        with open(path, 'wb') as fb:
            fb.write(content)

class MainHandler(tornado.web.RequestHandler):
    '''首页'''
    def get(self):
        self.write('<form action="/upload" enctype="multipart/form-data" method="post">'
                'Please specify a file, or a set of files: <br />'
                '<input type="file" name="file1" size="40" /><br />'
                '<input type="file" name="file2" size="40" /><br />'
                '<input type="submit" value="Submit">'
                )

class LoginHandler(tornado.web.RequestHandler):
    '''用户登陆页面'''

    def get(self):
        pass
    def post(self):
        pass

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", FileUploadHandler),
    (r"/login", LoginHandler),
    ], {'debug': True})

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

