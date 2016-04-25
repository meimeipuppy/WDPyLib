#berlvs.py
#@Class BerLvs
#@Author: mei yang
#@Creation: Feb-27-2014
from util.hexUtils import *
from bertlv import berLen, berHexLen
from berlv import *

class BerLvs():
    '''BerLvs is comprised of a number of BerLv object
        for exmample: 03aabbcc`023344`81A001..A0'''

    def __init__(self,string):
        self.lvList = []
        offset = 0
        while True:
            l = string[offset:offset+2]
            byteNum = berLen(l)
            if(byteNum==1):
                if(l==""):
                    vlen = 0
                else:
                    vlen = int(l,16)
            else:
                vlen = int(string[offset+2:offset+byteNum*2],16)
            wholeBytes = byteNum + vlen
            newoff = offset + wholeBytes*2
            if(newoff>len(string)):
                break
            self.lvList.append(BerLv(lv=string[offset:newoff]))
            offset = newoff
        self.lvs = string

    def getLvs(self):
        '''return lvs string'''
        return self.lvs
    
    def findLv(self, index):
        '''index starts from 1, return BerLv object'''
        return self.lvList[index-1]
    def getLvNumber(self):
        return len(self.lvList)
    
    def __str__(self):
        return self.lvs
    


if __name__ == "__main__":
    #6
    s = "010102112203112233041122334481A00102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f1000"
    lvs = BerLvs(s)
    print(lvs.getLvNumber()==6)
    print(str(lvs.findLv(3))=="03112233")
    print(str(lvs.findLv(1))=="0101")
    lv = lvs.findLv(5)
    print(str(lv)=="81A00102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    print(lv.getLength()==0xA0)
    print(lv.getValue()=="0102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f100102030405060708090a0b0c0d0e0f10")
    lv = lvs.findLv(6)
    print(str(lv)=="00")
    print(lv.getValue()=="")
    print(lv.getLength()==0)
    
