#!/usr/bin/python
#coding:utf8

import time

class StopWatch(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.__start = 0.0
        self.__second = 0.0

    def go(self):
        if self.__start == 0.0:
            self.__start = time.time()

    def reset_go(self):
        self.reset()
        self.go()

    def pause(self):
        if self.__start != 0.0:
            now = time.time()
            self.__second = (now - self.__start)
            self.__start = 0.0

    def get(self):
        '''return millsecond (毫秒)'''
        second = self.__second
        if self.__start != 0.0:
            now = time.time()
            second += (now - self.__start)
        return second * 1000

def main():
    watch = StopWatch()
    watch.go()

    print watch.get()
    time.sleep(1.5)
    print watch.get()
    time.sleep(1.5)
    print watch.get()

    watch.pause()
    time.sleep(1.5)
    print watch.get()

if __name__ == '__main__':
    main()

