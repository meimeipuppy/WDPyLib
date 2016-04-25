#@Class MixTlvs
#@Author: mei yang
#@Creation: March-5-2014
from util.hexUtils import *
from bertlvs import *


class MixTlvs(BerTlvs):
    '''mix tlvs structure:
        Tag: one or two bytes. can set a two-byte tag list to help program
            to identify the tlvs
        for example: C70133`5F20023344`DD0144
    '''

    def __init__(self, string, tbTagList):
        '''break MixTlvs into BerTlv list
            string: tlvs string
            tbTagList: two-byte tag list
        '''

        self.string = string
        self.indexPnt = 0 # gloabl pointer to the list index
        self.tlvList = []
        tagOffset = 0
        while tagOffset < len(string):
            tag = string[tagOffset:tagOffset+4]
            if(tag in tbTagList):
                tagLen = self.tagLen = 2;
            else:
                tagLen = self.tagLen = 1;
            wholeLen = tagLen + BerTlvs.getBytesOfLen(self,tagOffset)\
                       + BerTlvs.getVLen(self,tagOffset)
            newOffset = tagOffset + wholeLen*2
            if(newOffset>len(string)):
                break
            tlv = BerTlv(string[tagOffset:newOffset],taglen=tagLen)
            self.tlvList.append(tlv)
            tagOffset = newOffset

if __name__ == "__main__":
    #1
    print("test tag length=1")
    s = "8E01338F100102030405060708090a0b0c0d0e0f109003112233"
    tlvs = MixTlvs(s,[]) # empty tb tag list
    tlv = tlvs.findTlv("8E")
    #print(tlvs.tlvList[:])
    print(tlv.getTag()=="8E")       
    print(str(tlv)=="8E0133")       
    print(tlv.getLength()==1)       
    tlv = tlvs.findTlv("90")
    print(tlv.getTag()=="90")       
    print(str(tlv)=="9003112233")   

    #2
    print("test tag length = 2")
    s = "8E8E01338F8F100102030405060708090a0b0c0d0e0f10909000"
    tlvs = MixTlvs(s,['8E8E','8F8F','9090'])
        #test lower letter
    tlv = tlvs.findTlv("8e8e")
    print(tlv.getTag()=="8E8E")       
    print(str(tlv)=="8E8E0133")       
    print(tlv.getLength()==1)         
    tlv = tlvs.findTlv("9090")
    print(tlv.getTag()=="9090")     
    print(str(tlv)=="909000")        
    tlv = tlvs.findTlv("90")
    print(tlv==None)                  
    print(str(tlvs))

    tlv = tlvs.findTlvByIndex(2)
    print(str(tlv)=="8F8F100102030405060708090a0b0c0d0e0f10")
    tlv = tlvs.findTlvByIndex(3)
    print(str(tlv)=="909000")

    #3
    print("test tag length = 1&2")
    s = "8E8E01338F100102030405060708090a0b0c0d0e0f10909000"
    tlvs = MixTlvs(s,['8E8E','9090'])
        #test lower letter
    tlv = tlvs.findTlv("8e8e")
    print(tlv.getTag()=="8E8E")       
    print(str(tlv)=="8E8E0133")       
    print(tlv.getLength()==1)
    tlv = tlvs.findTlv("8F8F")
    print(tlv==None)
    tlv = tlvs.findTlv("8F")
    print(tlv.getLength()==16)
    print(str(tlv)=="8F100102030405060708090a0b0c0d0e0f10")
    tlv = tlvs.findTlv("9090")
    print(tlv.getTag()=="9090")     
    print(str(tlv)=="909000")        
    tlv = tlvs.findTlv("90")
    print(tlv==None)                  
    print(str(tlvs))

    tlv = tlvs.findTlvByIndex(2)
    print(str(tlv)=="8F100102030405060708090a0b0c0d0e0f10")
    tlv = tlvs.findTlvByIndex(3)
    print(str(tlv)=="909000")
