'''
Created on 2015年8月3日

@author: sunshyran
'''


import socket

from framework.channel.Acceptor import AbstractChannelAccepter
from framework.channel.Channel import AbstractChannel
from framework.channel.Connector import AbstractChannelConnector


class SocketChannel(AbstractChannel):
    '''
    classdocs
    '''


    def __init__(self, socket,addr):
        '''
        Constructor
        '''
        super().__init__()
        self.socket = socket
        self.addr = addr
      
        
    def send(self, data):
        '''
        send data. if error occurred, raise Exception
        '''
        #print('send', bytes(data, encoding = "utf8"))
        return self.socket.sendall(data)
    
    
    def recv(self):
        '''
        recv data. if error occurred, raise Exception
        '''
        #print("conn start recv")
        s = self.socket.recv(32*1024)
        #print('recv', s)
        return s
    
    
    def close(self):
        '''
        close channel
        '''
        print('channel %s is closed' % str(self.addr))
        return self.socket.close()
    
    
    def __str__(self):
        return str(self.socket) + str(self.addr)
    


class SocketChannelConnector(AbstractChannelConnector):
       
       
    def __init__(self, host, port):
        '''
        Constructor
        '''
        super().__init__()
        self._host = host
        self._port = port
    
    
    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._host, self._port))
        return SocketChannel(s, s.getsockname())

    
    
class SocketChannelAcceptor(AbstractChannelAccepter):
    def __init__(self, host, port):
        '''
        Constructor
        '''
        super().__init__()
        self._host = host
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self._host, self._port))
        self.sock.listen(5)


    def accept(self):
        conn, addr = self.sock.accept()
        return SocketChannel(conn, addr)
            
        
        
if __name__ == '__main__':
    conn = SocketChannelConnector('127.0.0.1', 12345).connect()
    print(conn)
    
    