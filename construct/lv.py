#lv.py
#@Class Lv
#@Author: mei yang
#@Creation: Feb-26-2014
from util.hexUtils import *

class Lv():
    '''lv structure: Length(1-byte)+Data(x-byte)'''

    def __init__(self,**kwargs):
        '''Lv(value=string) or Lv(lv=string);
            length: bytes of value
            value: data
        '''
        if(kwargs.has_key('value')):
            self.value = kwargs['value']
            self.length = len(self.value)/2
        elif(kwargs.has_key('lv')):
            self.length = int(kwargs['lv'][0:2],16)
            self.value = kwargs['lv'][2:]

    def getLength(self):
        return self.length

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.__init__(value=value)

    def __str__(self):
        return toHexByteStr(self.length)+self.value


if __name__ == "__main__":
    print("constructor 1")
    lv = Lv(value="3132")
    print(str(lv)=="023132")
    print(lv.getValue()=="3132")
    print(lv.getLength()==2)

    print("constructor 2")
    lv = Lv(lv="0701020304050607")
    print(lv.getLength()==7)
    print(str(lv)=="0701020304050607")
    lv.setValue("3344")
    print(lv.getValue()=="3344")
    print(str(lv)=="023344")

    print("test empty")
    lv = Lv(value="")
    print(str(lv)=="00")
    
