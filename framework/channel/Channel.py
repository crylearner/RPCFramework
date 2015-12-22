'''
Created on 2015年8月2日

@author: sunshyran
'''

class AbstractChannel(object):
    '''
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
        
        
    def send(self, data):
        '''
        send data. <p>
        if error occurred raise ChannelBrokenError. if channel is closed already, raise ChannelClosedError
        '''
        raise NotImplementedError
    
    
    def recv(self):
        '''
        recv data. 
        if error occurred raise ChannelBrokenError. if channel is closed already, raise ChannelClosedError
        '''
        raise NotImplementedError
    
    
    def close(self):
        '''
        close channel
        '''
        raise NotImplementedError
    
    

            