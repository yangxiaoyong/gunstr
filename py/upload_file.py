#encoding:utf8

#TODO:
# 1. 写出上传的WEB表单页面
# 2. 处理上传表单
# 3. 转存上传的文件
# 4. 用户认真

import os.path

import tornado.ioloop
import tornado.web

CWD = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = '/tmp'
SECRET_FILE = os.path.join(CWD, 'secret.txt')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class FileUploadHandler(BaseHandler):
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

    # TODO: 提交表单后给出超链接的访问清单
    #

class MainHandler(BaseHandler):
    '''首页'''

    @tornado.web.authenticated
    def get(self):
        self.write('<html><body>'
                '<a href="/logout">Logout</a><br />'
                'Welcome %s '
                '<form action="/upload" enctype="multipart/form-data" method="post">'
                'Please specify a file, or a set of files: <br />'
                '<input type="file" name="file1" size="40" /><br />'
                '<input type="file" name="file2" size="40" /><br />'
                '<input type="submit" value="Submit">'
                '</form>'
                '</body></html>'
                % tornado.escape.xhtml_escape(self.current_user)
                )

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')

class LoginHandler(BaseHandler):
    '''用户登陆页面'''

    def get(self):
        self.write('<html><body>'
                '<form action="/login" method="post">'
                '<p>Login</p>'
                '<label for="username">Username: </label>'
                  '<input type="text" id="username" name="username" />'
                '<label for="password">Password: </label>'
                  '<input type="password" id="password" name="password" />'
                '<input type="submit" value="Sign in" />'
                '</form>'
                '</body></html>'
                )

    def post(self):
        '''
        user:pwd
        '''
        username = self.get_argument("username")
        password = self.get_argument("password")
        with open(SECRET_FILE) as fb:
            for line in fb:
                user, pwd = line.strip().split(':')
                if user == username:
                    if pwd == password:
                        self.set_secure_cookie("user", user)
                        self.redirect("/")
                    else:
                        self.write("Password does not match")
                else:
                    self.write("User does not exists")

settings = {
        "cookie_secret": "b508680bae35614a88cafdb489b17aeb",
        "login_url": "/login",
        "debug": True,
        }

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", FileUploadHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    ], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

