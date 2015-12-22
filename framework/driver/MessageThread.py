'''
Created on 2015年7月19日

@author: sunshyran
'''
import threading


class MessageFullError(Exception):
    pass
    

class MessageEmptyError(Exception):
    pass


class StopError(Exception):
    pass


class MessageThread(threading.Thread):
    '''
    a message thread。是一个阻塞的消息队列模型，FIFO
    '''


    def __init__(self, name, target):
        '''
        Constructor
        '''
        super().__init__(name=name, target=target, daemon=True)
        self.messages = []
        self._capacity = 1024*1024*1024 # 消息列表的最大长度
        self.locker = threading.Condition() # 多线程锁
        self.isrunning = False
        
    
    def capacity(self):
        '''
        max count message can be hold
        '''
        return self._capacity
    
    
    def setCapacity(self, capacity):
        self._capacity = capacity
    

    def size(self):
        '''
        return message count
        '''
        return len(self.messages)
    
    
    def empty(self):
        '''
        return if no message contains
        '''
        return len(self.messages) == 0
    
    
    def clear(self):
        '''
        remove all messages.NOTE:: can work well even message thread is stopped
        '''
        with self.locker:
            self.messages.clear()
      
      
    def isRunning(self):
        '''
        return if messsage thread is running
        '''
        return self.isrunning
      
       
    def start(self):
        '''
        \ 启动消息队列，内部会自动启动一个线程
        '''
        # 先设置isrunning,否则有可能会先执行pop_message(),从而意外返回一个None
        with self.locker:
            if self.isrunning: return 
            self.isrunning = True
        super().start()
        print("Message thread(%s) is started\n" % self.getName())
        
        
    def stop(self):
        '''
        \ 停止消息队列.立即返回，并不等待线程结束
        ''' 
        with self.locker:
            if not self.isrunning: return
            self.isrunning = False
            self.locker.notify() # 必须的，告诉pop_message，状态变化了。保证pop_message不会一直阻塞
        print("Message thread(%s) is stopping\n" % self.getName())
        
    
    def stopAndWait(self):
        self.stop()
        self.join()
        print("Message thread(%s) is stopped\n" % self.getName())
       
        
    def push(self, msg, timeout=None):
        '''
        push a message into　queue
        @note: 如果当前消息队列已满，则会阻塞，一直等到不满或者超时。
        @param timeout: 超时时间。如果超时，则raise MessageFullError()
        '''
        with self.locker:
            while self.isrunning and len(self.messages) >= self._capacity:
                if not self.locker.wait(timeout):
                    print('Message thread:%s push message %s timeout' %(self.getName(), msg)) 
                    raise MessageFullError(self.getName() + " : message queue is full")
                
            if not self.isrunning: raise StopError(self.getName() + ' is stopped')
            
            self.messages.append(msg)
            self.locker.notify()
            
            
    def pop(self, timeout=None):
        '''
        pop a message from queue
        @return: None表示该消息队列已停止运行，否则返回一个最先进入的消息（FIFO）
        '''
        with self.locker:
            while self.isrunning and len(self.messages) == 0 : 
                if not self.locker.wait(timeout):
                    print('Message thread:%s pop message timeout' %self.getName()) 
                    raise MessageEmptyError(self.getName() + " : message queue is empty")
                
            if not self.isrunning: raise StopError(self.getName() + ' is stopped')
            return self.messages.pop(0)
   
   
if __name__ == '__main__':
    print(MessageFullError('message full'))
    print(MessageEmptyError('message empty'))
    print(StopError('message thread stop'))
    
 
        