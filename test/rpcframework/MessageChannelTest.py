'''
Created on 2015年12月22日

@author: sunshyran
'''
import unittest

from framework.assembly.Assembly import Assembly
from framework.channel.MessageChannel import RpcMessageChannel
from test.rpcframework.FakeChannel import FakeChannel
from test.rpcframework.FakeDeserializer import FakeDeserializer
from test.rpcframework.FakeSerializer import FakeSerializer


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test(self):
        channel = RpcMessageChannel(FakeChannel(), FakeSerializer(), FakeDeserializer(), Assembly())
        channel.send('msg1')
        channel.send('msg2')
        msg1 = channel.recv()
        msg2 = channel.recv()
        self.assertTrue(msg1=='msg1', msg1)
        self.assertTrue(msg2=='msg2', msg2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()