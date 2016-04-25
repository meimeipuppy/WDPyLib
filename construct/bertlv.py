#bertlv.py
#@Class BerTlv
#@Author: mei yang
#@Creation: Feb-24-2014
from util.hexUtils import *


class BerTlv():
    '''a BerTlv object is comprised of
        Tag(support 1-N bytes);
        Leng, support 81,82;
        Value: string value
        getTag()
        getLength()
        getLenHex()
        getValue()
        str()
        
        
    '''
    def __init__(self, *args, **kwargs):
        '''two constructors: BerTlv(tag, value) or BerTlv(string, taglen=x)'''
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        if(kwargs=={}):
            self.tag = args[0]
            self.value = args[1]
            l = len(self.value)/2
            self.vlen = l
            self.length = berHexLen(l)

        elif(kwargs["taglen"]==0):
            raise InputError(0)
        else:
            string = args[0]
            tLen = kwargs["taglen"]
            self.tag = string[0 : 2*tLen]
            ll = string[2*tLen : 2*(tLen+1)]
            bytenum = berLen(ll)
            offset = 2*(tLen+bytenum)
            self.length = string[2*tLen :offset]
            self.value = string[offset:]
            self.vlen = len(self.value)/2
        
    def getTag(self):
        '''get the tag string'''
        return self.tag

    def getLength(self):
        '''get the length of value string in hex bytes'''
        return self.vlen
    
    def getLenHex(self):
        '''get the value length in hex, eg:'03', '81EF','820133' '''
        return self.length

    def getValue(self):
        '''get the value string'''
        return self.value
        
    def getBytesOfLen(self):
        return len(self.length)/2
        
    def __str__(self):
        return self.tag+self.length+self.value

    def getTotalLen(self):
        '''total length of tag, length and value in byte'''
        return len(str(self))/2

    def setTag(self, tag):
        self.tag = tag

    def setValue(self, value):
        self.value = value
        self.__init__(self.tag, value)    

    def setOptional(self, attribute=True):
        '''set this tlv optional in the data structure'''
        self.optional = attribute

    def isOptional(self):
        return self.optional

def berLen(firstByte):
    '''return how many bytes of length field'''
    if(firstByte=="81"):
        return 2
    elif(firstByte=="82"):
        return 3
    else:
        return 1
def berHexLen(length):
    '''return 00-80,8100-81FF,820100-82FFFF according to the int length'''
    if(length<0x80):
        return toHexByteStr(length)
    elif(length>0x7F and length<0x100):
        return "81"+toHexByteStr(length)
    elif(length>0x100):
        return "82"+toHexByteStr(length)
    

class InputError(Exception):
    def __init__(self,param):
        self.message = param

    def __str__(self):
        return "bad parameter: "+repr(self.param)
        

if __name__ == "__main__":
    #test constructor #1
    tlv = BerTlv("3E", "010203040506")
    print(tlv.getTag())        #3E
    print(tlv.getLength())     #6
    print(tlv.getValue())      #01..06
    print(str(tlv))            #3E0601..06
    print(tlv.getTotalLen())   #8
    print(tlv.getBytesOfLen()) #1
    tlv.setTag("89")
    tlv.setValue("0102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    print(tlv.getTag())        #89
    print(tlv.getValue())      #01...06
    print(tlv.getTotalLen())   #163
    print(tlv.getBytesOfLen()) #2
    print(str(tlv))      #8981A001..06
    print(tlv.getLenHex())     #81A0

    #test constructor #2
    tlv = BerTlv("8981A00102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10"
                 ,taglen=1)
    print(tlv.getTag())        #89
    print(tlv.getValue())      #01...06
    print(tlv.getTotalLen())   #163
    print(tlv.getBytesOfLen()) #2
    print(str(tlv))      #8981A001..06
    print(tlv.getLenHex())     #81A0    

    #test 2-byte tag
    tlv = BerTlv("8E8F03010203", taglen=2)
    print(tlv.getTag())        #8E8F
    print(tlv.getValue())      #010203
    print(tlv.getTotalLen())   #6
    print(tlv.getBytesOfLen()) #1
    print(str(tlv))      #8E8F03010203
    print(tlv.getLenHex())     #03

    #test length=0
    tlv = BerTlv("FE","")
    print(str(tlv))      #FE00
    tlv = BerTlv("EF00", taglen=1)
    print(str(tlv))      #EF00
    print(tlv.getValue())      #""
    print(tlv.getValue()=="")  #true
