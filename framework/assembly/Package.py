'''
Created on 2015-5-25

@author: 23683
'''
import struct


class RpcPackage(object):
    '''
    package used to transmit on channel.
    \ 由于tcp长链接会出现粘包、半包的问题，因此加入专门的头、size、尾 方便定位
    '''

#    pack_format='@'
#                + 'BBBB' #'@RPC'
#                + 'L' #message size, NOT include head and tail
#                + 's' #rpc message
#                + 'BBBB' #'#rpc'
 
    pack_format= '4sL%ds4s'
    HAED  = b'RPC@'
    TAIL  = b'#rpc'
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.message        = bytes()  # rpc message that has been serialized
        
    
    def __str__(self):
        return str(bytes().join((self.HAED, self.message, self.TAIL)))
    
    
    @classmethod
    def minSize(cls):
        return struct.calcsize(cls.pack_format % 0)
    
    
    def encode(self):
        '''
        return bytes object of the pacakge
        '''
        messagelen = len(self.message)
        packformat=self.pack_format % messagelen
        #print(packformat)
        return struct.pack(packformat, self.HAED, messagelen, self.message, self.TAIL)
        
        
    def decode(self, databytes):
        '''
        decode
        '''
        try:
            (head, size) = struct.unpack('<4sL', databytes[0:8])
            if head != self.HAED:
                print("Error package")
                return 
            format = '<%ds4s' % size
            (message, tail) = struct.unpack(format, databytes[8:])
            if tail != self.TAIL:
                print("Error package")
                return 
            
            self.message = message
        except Exception as e:
            print(e)
            return None
        
        
        
if __name__ == '__main__':
    print(RpcPackage.minSize())
    package = RpcPackage()
    package.message = b'abc'
    print(package)
    print(package.encode())
    package2 = RpcPackage()
    package2.decode(b'RPC@\x03\x00\x00\x00abc#rpc')
    print(package2)
    
    
    
    