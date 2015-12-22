'''
Created on 2015年7月12日

@author: sunshyran
'''
from framework.driver.MessageDriver import AbstractMessageDriver
from framework.driver.MessageThread import MessageThread, StopError,\
    MessageFullError, MessageEmptyError



class InvokerHandler(AbstractMessageDriver):
    '''
    \ 支持异步的RPC消息处理者。 一方面负责自动将消息从这端发送出去，另一方面负责自动从对端接收RPC消息
    \ 内部通过引入两个线程以及对应的消息队列，实现消息的发送和接收并行。
    '''
    
    DEFAULT_TIMEOUT = None
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.invoking_thread = MessageThread(target=self.__dealing_invoker, name='invoking')
        self.retrieving_thread = MessageThread(target=self.__receive_invoker, name='retrieving')
        self.isrunning = False
        
    
    def startup(self):
        '''
        
        '''
        print("MessageHandler startup")
        self.isrunning = True
        self.invoking_thread.start()
        self.retrieving_thread.start()
        
        
    def shutdown(self):
        print("MessageHandler shutdown")
        self.isrunning = False
        # 必须先停止依赖的数据通道，然后才能停止发送和接收线程
        self.channel.close() 
        self.invoking_thread.stopAndWait()
        self.retrieving_thread.stopAndWait()
        
        
        
    def invoke(self, invoker):
        '''
        \ 将invoker放入invoker处理队列
        @return True means OK, otherwise return False or raise Exception
        '''
        if not self.isrunning: raise Exception()
        try:
            self.invoking_thread.push(invoker, self.DEFAULT_TIMEOUT)
        except MessageFullError as e:
            print(e)
        except StopError as e:
            raise 
        
    
    def retrieve(self):
        '''
        \ 从retrieve队列中取出一个消息。 
        @note: 会一直阻塞，直到取到一个
        @return: return a message. If failed for some reason, exception will be raised
        '''
        if not self.isrunning: raise Exception()
        try: 
            message = self.retrieving_thread.pop(self.DEFAULT_TIMEOUT)
            return  message
        except MessageEmptyError as e:
            print(e)
        except StopError as e:
            raise 
    
    
    def __dealing_invoker(self):
        while self.isrunning:
            try:
                invoker = self.invoking_thread.pop()
                print('1111')
                self.channel.send(invoker.message)
                print('2222')
            except StopError:
                print('warning: message thread is broken')
                self.isrunning = False
                break
            except Exception as e:
                print(e)
                print('stop invoking thread')
                self.isrunning = False
                break
         
            
    def __receive_invoker(self):
        while self.isrunning:
            try :
                print('3333')
                message = self.channel.recv()
                self.retrieving_thread.push(message)
                print('4444')
            except StopError:
                print('stop retrieving thread')
                self.isrunning = False
                break        
            except Exception as e:
                print(e)
                print('stop retrieving thread')
                self.isrunning = False
                break
            
