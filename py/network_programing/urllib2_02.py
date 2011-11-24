import urllib2

# create request object which represents the HTTP request you are making
# there two extra things that Request objects allow you can do:
# 1. you can pass data to be sent to the server.
# 2. you can pass extra information("metadata") about the data or request itself. to
#    the server this information is sent ad HTTP "headers" .
req = urllib2.Request("http://python.org")
response = urllib2.urlopen(req)

the_page = response.read()
print the_page
