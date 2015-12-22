'''
Created on 2015年12月12日

@author: sunshyran
'''

    
    
class AbstractChannelAccepter(object):
     
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
        
    def accept(self):
        '''
        \用于接收来自对端的channel创建请求，并返回channel
        '''
        raise  NotImplementedError
    
