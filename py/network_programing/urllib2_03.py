import urllib
import urllib2

url = 'http://localhost:8888/login'
values = {'username': 'yxy',
          'password': '123'}

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page
