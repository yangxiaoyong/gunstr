def cycle(iterable):
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
        print saved

    while saved:
        for element in saved:
            yield element

c = cycle('ABCD')
for i in range(10):
    print c.next()
