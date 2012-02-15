import xmlrpclib
proxy = xmlrpclib.ServerProxy('http://localhost:8080')
url = proxy.cmd_get_new_monitor_url('hello')
print url
