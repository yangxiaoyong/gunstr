class A:
    def __init__(self):
        print 'Init A'

class B(A):
    # will error
    def __init__(self):
        # call the super function ,the arg[0] must be a object not a classobj
        super(A, self).__init__()

b = B()
