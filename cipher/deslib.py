#@Class DesLib
#@Author: meiyang
#@Creation: Feb-27-2016

from pyDes import *

class DesLib():
    '''
    do des/3des cbc/ecb encryption/decryption
    '''
    
    def __init__(self, *args):
        '''define some default values'''
        self.key = ""
        self.iv = "\0\0\0\0\0\0\0\0"
        self.ciphermode = ECB
        self.data = ""
        self.pad = None
        self.padmode = PAD_PKCS5


    def loadKey(self, key):
        self.key = key #string
    def init(self, ciphermode, iv, pad, padmode):
        self.ciphermode = ciphermode
        self.iv = iv
        self.pad = pad
        self.padmode = padmode
        self.desobject = des(self.key, \
                             self.ciphermode, \
                             self.iv, \
                             self.pad, \
                             self.padmode )
    def encrypt(data):
        return self.desobject.endrypt(data)

    def decrypt(cipherdata):
        return self.desobject.decrypt(data)
    
if __name__ == "__main__":
    print("testing 3des")
    deslib = DesLib()
    data = "0102030405060708090a0b0c0d0e0f10"
    key = "0123456789abcdeffedcba9876543210"
    
