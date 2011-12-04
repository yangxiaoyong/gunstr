class RevealAccess(object):
    """A data descriptior that sets and returns values
    normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='val'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print 'Retrieving', self.name
        return self.val

    def __set__(self, obj, val):
        print 'Updating', self.name
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'val "x"')
    y = 5

m = MyClass()
m.x
m.x = 20
m.x
m.y



