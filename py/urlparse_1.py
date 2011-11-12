# use urlparse to parse url
# will return 6 elments in one tuple
# schema://netloc/path;parameters?query#fragment
# (schema, netloc, path, params, query, fragment)

import urlparse

url = 'http://alice:secret@www.example.com:80;what/%7Ealice/index.cgi?q=text#sample'
r = urlparse.urlparse(url)
print r.params

url2 = 'python.org'
r2 = urlparse.urlparse(url2, 'http')

# join a url
r1 = urlparse.urljoin(url2, 'index.html')
