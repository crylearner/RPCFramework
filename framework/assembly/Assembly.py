'''
Created on 2015-8-10

@author: 23683
'''

import struct
from framework.assembly.Package import RpcPackage

class Assembly(object):
    '''
    \字节流的转配和组装器
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.data = bytearray()
    
    
    def assembleBytes(self, databytes):
        self.data += databytes
        print(self.data)
        try:
            if len(self.data) < RpcPackage.minSize():
                return None
            (head, size) = struct.unpack('<4sL', self.data[0:8])
            if head != RpcPackage.HAED:
                print("Error package")
                return None
            
            if len(self.data) < size + RpcPackage.minSize():
                return None
            pkt = RpcPackage()
            pkt.decode(self.data)

            # TODO::verify
            
            self.data = self.data[size + RpcPackage.minSize():]
            return pkt.message
        except Exception as e:
            print(e)
            return None
        
    
    def assembleMessage(self, message):
        package = RpcPackage()
        package.message = message
        return package.encode()
        

if __name__ == '__main__':
    data = b'RPC@\x03\x00\x00\x00abc#rpc'
    assembly = Assembly()
    result = assembly.assembleBytes(data[0:4])
    assert(result == None)
    result = assembly.assembleBytes(data[4:10])
    assert(result == None)
    result = assembly.assembleBytes(data[10:])
    print(result)
    
        