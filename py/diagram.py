from random import randint
from pprint import pprint

def column_diagram(word):
    size = len(word)
    print '%s: %s\n' % (word.ljust(50), '|' * size)

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = range(0, 10)

def rand_word():
    w = ''
    for i in range(randint(1, 50)):
        w += letters[randint(0, len(letters) - 1)]
    return w

def ver_diagram(word_arr):
    array = []
    for index, w in enumerate(word_arr):
        array.append([])
        for s in w:
            array[index].append(1)
        array[index].append(0)
    return array


array = []
for i in range(10):
    array.append(rand_word())
    # column_diagram(rand_word())
pprint(ver_diagram(array))


