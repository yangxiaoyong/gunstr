from SimpleXMLRPCServer import SimpleXMLRPCServer as s

def hello(name):
    return 'Hello, %s' % name

server = s(('localhost', 8080))
server.register_function(hello, 'hello')
server.serve_forever()
