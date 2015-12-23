'''
Created on 2015年12月13日

@author: sunshyran
'''
from framework.channel.Channel import AbstractChannel


class RpcMessageChannel(AbstractChannel):
    '''
    
    '''
    def __init__(self, channel, serializer, deserializer, assembler):
        '''
        RpcMessageChannel channel装饰器.
        @param serializer 序列化rpc message
        @param deserializer  反序列化rpc message
        @param assembler  channel层次传输用的装配器
        '''
        super().__init__()
        self._internal_channel = channel
        self.assembler = assembler
        self.serializer = serializer
        self.deserializer = deserializer
        
        
    def send(self, message):
        '''
        send data. <p>
        if error occurred raise ChannelBrokenError. if channel is closed already, raise ChannelClosedError
        '''
        
        package = self.assembler.assembleMessage(self.serializer.serialize(message))
        print('send ' + str(package))
        self._internal_channel.send(package)
        
    
    
    def recv(self):
        '''
        recv data. <p>
        if error occurred raise ChannelBrokenError. if channel is closed already, raise ChannelClosedError
        '''
        message = self.deserializer.deserialize(self.assembler.assembleBytes(self._internal_channel.recv()))
        print('recv ' + str(message))
        return message
    
    
    def close(self):
        '''
        close channel
        '''
        self._internal_channel.close()


