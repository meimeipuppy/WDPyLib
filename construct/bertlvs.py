#@Class BerTlvs
#@Author: mei yang
#@Creation: Feb-24-2014
#from util.hexUtils import *
from bertlv import *

class BerTlvs():
    '''BerTlvs object is comprised of multiple BerTlv.
        for example: E00133`E1023132`E203414243
        tag should have unified length, say, one or two bytes for each tlv element
        findTlv()
        
    '''
    def __init__(self, string, tagLen=1):
        '''break BerTlvs into BerTlv list
            tagLen is the length of tag in byte.
            default taglen is 1
        '''
        self.tagLen = tagLen
        self.string = string
        self.indexPointer = 0  #global Pointer to the list index
        self.tlvList = []
        tagOffset = 0
        while tagOffset < len(string):
            wholeLen = tagLen + self.getBytesOfLen(tagOffset)+ self.getVLen(tagOffset)
            newOffset = tagOffset+wholeLen*2
            if(newOffset>len(string)):
                break
            tlv = BerTlv(string[tagOffset:newOffset], taglen=tagLen)
            self.tlvList.append(tlv)
            tagOffset = newOffset
        #for_end
        #init_end
        
        
    def getBytesOfLen(self, tagoff):
        '''from the given tag offset(in character), caculate the length field in byte'''
        tagoff = tagoff + self.tagLen*2
        ll = self.string[tagoff : tagoff+2]
        return berLen(ll)
    
    def getVLen(self, tagoff):
        '''from the given tag offset(character), return value length in byte'''
        bytenum = self.getBytesOfLen(tagoff)
        tagoff = tagoff + self.tagLen*2
        #true length of value:
        ll = self.string[tagoff+bytenum*2-2 : tagoff+bytenum*2]
        return int(ll,16)
        
    def findTlv(self, tag):
        '''return found tlv object, if not, return none'''
        for tlv in self.tlvList:
            if(tlv.getTag().upper()==tag.upper()):
                return tlv
        return None

    def findTlvByIndex(self, index):
        '''index starts from 1'''
        return self.tlvList[index-1]

    def __str__(self):
        return self.string

if __name__ == "__main__":
    #1
    print("test tag length=1")
    s = "8E01338F100102030405060708090a0b0c0d0e0f109003112233"
    tlvs = BerTlvs(s,1)# = BerTlvs(s)
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
    tlvs = BerTlvs(s,2)
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
    
    
