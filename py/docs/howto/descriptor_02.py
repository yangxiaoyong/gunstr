class C(object):
    def __init__(self): self.__x = ''
    def getx(self): return self.__x
    def setx(self, value): self.__x = value
    def delx(self): del self.__x
    x = property(getx, setx, delx, "I'm the 'x' propetry")


c = C()
print c.x
c.x = 'xxx'
print c.x


