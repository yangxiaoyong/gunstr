#encoding:utf-8
# use urllib.quote to encode url which contains unsafe ASCII character

import urllib

u1 = '~/test /&q=text'
q1 = urllib.quote(u1)
q2 = urllib.quote_plus(u1)
qs = [q1,
      q2,
      urllib.unquote_plus(q2),
      urllib.unquote(q1)]

for i in qs:
    print i

# demo for chinese encodind
r = urllib.quote("中文编码")
print r
print urllib.unquote(r)

# query urlencod
# k1=v1&k2=v2
print urllib.urlencode([('k1', 'v1'), ('k2', 'v2')])
print urllib.urlencode({'k1': 'v1', 'k2': 'v2'})
