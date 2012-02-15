#-*- encoding:utf-8 -*-
import time
import multiprocessing

from datetime import datetime

'''
oscillator 类接受一个代理对象，变量event
代理对象是multiprocessing.Manger类返回的一个实例
multiprocessing.Manager 可以让不同的进程共享状态和数据并且也支持其它数据
类型共享，比如： list, dict, NameSpace, Lock, RLock, Semaphore, Condition,
Event, Queue, Value, 和 Array,。除 list, dict, 和 NameSpace ，其它所有的
类型都是threading库里的对应原子类型的clone
'''

class Oscillator(multiprocessing.Process):
    '''The Oscillator class generates events at defined intervals'''
    def __init__(self, event, period):
        self.period = period
        self.event = event
        super(Oscillator, self).__init__()

    def run(self):
        try:
            while True:
                self.event.clear()
                time.sleep(self.period)
                self.event.set()
        except KeyboardInterrupt:
            pass

class Schedule(multiprocessing.Process):
    '''The Schedule class listens to periodic events'''
    def __init__(self, event):
        self.event = event
        super(Schedule, self).__init__()

    def run(self):
        try:
            while True:
                self.event.wait()
                print datetime.now()
        except KeyboardInterrupt:
            pass

mgr = multiprocessing.Manager()
e = mgr.Event()
o = Oscillator(e, 1)
s = Schedule(e)
o.start()
s.start()
try:
    while len(multiprocessing.active_children()) != 0:
        time.sleep(1)
except KeyboardInterrupt:
    o.terminate()
    s.terminate()
o.join()
e.join()

