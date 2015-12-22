'''
Created on 2015年12月17日

@author: sunshyran
'''



class AbstractDeserializer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        
        
    def deserialize(self, bytestring):
        '''
        return concrete rpc message,  e.g. Request, Response, Notification
        '''
        raise NotImplementedError
    