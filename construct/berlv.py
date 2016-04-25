#berlv.py
#@Class BerLv
#@Author: mei yang
#@Creation: Feb-27-2014
from util.hexUtils import *
from bertlv import berLen, berHexLen

class BerLv():
    '''BerLv: length 00-7F,8180-81FF,820100-82FFFF; value'''
    def __init__(self, **kwargs):
        '''BerLv(value=string) or BerLv(lv=string);
            length: bytes of data
            data: data
        '''
        if(kwargs.has_key('value')):
            self.value = kwargs['value']
            self.length = len(self.value)/2
            self.hexLen = berHexLen(self.length)
        elif(kwargs.has_key('lv')):
            l = berLen(kwargs['lv'][0:2]) #bytes of hexlen
            self.length = len(kwargs['lv'][l*2:])/2
            self.value = kwargs['lv'][l*2:]
            self.hexLen = kwargs['lv'][0:l*2]

    def getValue(self):
        return self.value
    
    def getLength(self):
        return self.length

    def setValue(self,value):
        self.__init__(value=value)
    
    def __str__(self):
        return self.hexLen+self.value
    

if __name__ == "__main__":
    print("test constructor 1")
    lv = BerLv(value="33445566778899")
    print(str(lv)=="0733445566778899")
    print(lv.getValue()=="33445566778899")
    print(lv.getLength()==7)

    lv.setValue("0102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    print(lv.getLength()==0xA0)
    print(str(lv)=="81A00102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")

    print("test constructor 2")
    lv = BerLv(lv="81A00102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    print(lv.getLength()==0xA0)
    print(lv.getValue()=="0102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    print(str(lv)=="81A00102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    lv.setValue("0102")
    print(lv.getValue()=="0102")
    print(lv.getLength()==2)
    print(str(lv)=="020102")

    print("test empty")
    lv = BerLv(value="")
    print(lv.getValue()=="")
    print(lv.getLength()==0)
