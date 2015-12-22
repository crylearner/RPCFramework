'''
Created on 2015年8月2日

@author: sunshyran
'''


import threading

class AbstractClient(object):
    
    def __init__(self, invoker_handler):
        self.handler = invoker_handler
        
    
    def start(self):
        self.handler.startup()
        self.thread = threading.Thread(target = self.retrieveResponse, daemon = True)
        self.thread.start()
        
        
    def stop(self):
        print('ppppp')
        self.handler.shutdown()
        self.thread.join()
    
    
    def run(self):
        pass
    
    
    def request(self, invoker, timeout=5000):
        '''
        \ 同步阻塞调用，返回Response
        '''
        raise NotImplementedError
    
    
    def asyncrequest(self, invoker):
        '''
        \ 异步非阻塞调用，返回None。结果处理由responseListener负责
        '''
        self.handler.invoke(invoker)
        return None
    
    
    def retrieveResponse(self):
        while True:
            print('tttt')
            msg = self.handler.retrieve()
            self.onResponse(msg)
        
        
    def onResponse(self, rsp):
        raise NotImplementedError()
    
            
#     def listen(self, listener):
#         return self.listener_manager.register(listener)
#     
#     def cancelListener(self, listener):
#         return self.listener_manager.unregister(listener)
#             
#     def get_identity(self, listener):
#         return self.listener_manager.get_identity(listener)
#     
        