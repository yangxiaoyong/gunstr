class Fruit:
    def __init__(self, color):
        self.__color = color
        print self.__color

    def __del__(self):
        self.__color = ""
        print "free"

    def grow(self):
        print "grow"

if __name__ == "__main__":
    fruit = Fruit('red')
    fruit.grow()
    fruit.grow()



