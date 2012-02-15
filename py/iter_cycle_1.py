from itertools import cycle

def get_line(fp):
    with open(fp) as fb:
        for line in fb:
            yield line

lines = cycle(get_line('iter_cycle.py'))
print lines.next()
print lines.next()
print lines.next()
print lines.next()
print lines.next()
print lines.next()
print lines.next()
print lines.next()
print lines.next()
