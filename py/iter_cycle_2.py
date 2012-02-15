def cycle():
    li = [1, 2, 3, 4, 5]
    while li:
        for element in li:
            yield element

c = cycle()
for i in range(10):
    print c.next()
