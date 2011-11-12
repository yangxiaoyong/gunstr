# 访问需要简单认证的weba资源

import urllib

class MyURLOpener(urllib.FancyURLopener):

    def setAuth(self, user, passwd):
        self,user = user
        self.passwd = passwd

    def prompt_user_password(self, host, realm):
        '''return user and password'''
        return self.user, self.passwd

# 自定义头元信息
opener = urllib.FancyURLopener()
opener.addheader('User-Agent', 'Mozilla/4.0 (compaxxxx)')
opener.addheader('Accept', 'text/html')
opener.addheader('Connection', 'close')
opener.open('http://www.google.com')

