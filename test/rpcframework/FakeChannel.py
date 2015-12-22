'''
Created on 2015年12月22日

@author: sunshyran
'''
import threading

from framework.channel.Channel import AbstractChannel
from framework.channel.Exception import ChannelClosedError


class FakeChannel(AbstractChannel):
    
    def __init__(self):
        super().__init__()
        self.msg = []
        self.isclosed = False
        self.locker = threading.Condition()
    
    
    def send(self, data):
        if self.isclosed: raise ChannelClosedError()
        self.msg.append(data)
        with self.locker: self.locker.notifyAll()
    
    
    def recv(self):
        with self.locker:
            while (not self.isclosed) and len(self.msg) == 0:
                self.locker.wait(1)
            if self.isclosed: raise ChannelClosedError()
        return self.msg.pop(0)
    
    def close(self):
        self.isclosed = True


if __name__ == '__main__':
    c = FakeChannel()
    c.send('a')
    assert('a' == c.recv())
    c.close()
    print(c.recv()) # raise  exception
    