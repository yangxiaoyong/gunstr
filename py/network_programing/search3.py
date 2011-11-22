#!/usr/bin/env python

import httplib

try:
    import json
except ImportError:
    import simplejson as json

path = ('/maps/geo?q=207+N.+Defiance+St%2C+Archbold%2C+OH'
        '&output=json&oe=utf8')

connection = httplib.HTTPConnection('maps.google.com')
connection.request('GET', path)
rawreply = connection.getresponse().read()
reply = json.loads(rawreply)
print reply
