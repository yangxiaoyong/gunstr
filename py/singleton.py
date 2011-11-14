# 实现单例模式

class Singleton(object):
    __instance = None

    def __new__(cls, *args, **kws):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls, *args, **kws)
        return Singleton.__instance

