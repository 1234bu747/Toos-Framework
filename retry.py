# -*-coding:utf-8 -*-
import time

def retry(times):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            i = 0
            while i < times:
                try:
                    print(u"第{}次尝试：{}".format(i + 1, func.__name__))
                    return func(*args, **kwargs)
                except Exception as error:
                    print("logdebug:{}{}".format(func.__name__, error))
                    # log.error("logdebug:{}{}".format(func.__name__, error))
                    time.sleep(2)
                    i += 1

        return inner_wrapper

    return wrapper


@retry(10)
def a(b):
    print(1 + b)


a(3)
