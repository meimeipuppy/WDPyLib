#apdu.py
#@Class APDU
#@Author: mei yang
#@Creation: Feb-25-2014

from util.hexUtils import toHexByteStr

class APDU():
    '''APDU object: CLA INS P1 P2 LC DATA

    '''
    def __init__(self, *args):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        '''two constructors:
            APDU(byte CLA,byte INS,byte P1,byte P2,string DATA)
            APDU(string apdu)

        '''
        if(len(args)==5): #1
            self.cla=args[0]
            self.ins=args[1]
            self.p1=args[2]
            self.p2=args[3]
            self.data=args[4]
            self.lc=len(self.data)/2
            
        if(len(args)==1): #2
            apdu = args[0]
            self.cla = int(apdu[0:2],16)
            self.ins = int(apdu[2:4],16)
            self.p1 = int(apdu[4:6],16)
            self.p2 = int(apdu[6:8],16)
            self.lc = int(apdu[8:10],16)
            self.data = apdu[10:]

    def getCla(self):
        '''int'''
        return self.cla
    def getIns(self):
        '''int'''
        return self.ins
    def getP1(self):
        '''int'''
        return self.p1
    def getP2(self):
        '''int'''
        return self.p2
    def getLc(self):
        '''int'''
        return self.lc
    def getData(self):
        '''string'''
        return self.data
    
    def __str__(self):
        return toHexByteStr(self.cla)\
                +toHexByteStr(self.ins)\
                +toHexByteStr(self.p1)\
                +toHexByteStr(self.p2)\
                +toHexByteStr(self.lc)\
                +self.data



    
if __name__ == "__main__":
    print("test short apdu")
    apdu = APDU(0,0x8E,0,1,"3E3F4243")
    print(str(apdu)=="008E0001043E3F4243")

    print("test long apdu")
    apdu = APDU(0,0x94,2,4,"000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f")
    print(str(apdu))
    print(apdu.getCla()==0)
    print(apdu.getIns()==0x94)
    print(apdu.getP1()==2)
    print(apdu.getP2()==4)
    print(apdu.getLc()==0xa0)
    
    print("test constructor#2")
    apdu = APDU("00940204a0000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f000102030405060708090a0b0c0d0e0f")
    print(str(apdu))
    print(apdu.getCla()==0)
    print(apdu.getIns()==0x94)
    print(apdu.getP1()==2)
    print(apdu.getP2()==4)
    print(apdu.getLc()==0xa0)
    
