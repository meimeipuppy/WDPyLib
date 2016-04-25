#@Class Element
#@Author: mei yang
#@Creation: March-5-2014

from bertlv import *

class Element:
    ''' a node includes title, a BerTlv value, and an interpretation of
its value '''
    def __init__(self):
        self.title = None
        self.tlv = None
        self.interpretation = None
        
    def setTitle(self,string):
        self.title = string

    def setValue(self,tlv):
        self.tlv = tlv

    def setInterpretation(self,string):
        self.interpretation = string
        
    def getTitle():
        return self.title
    def getValue():
        '''return a BerTlv structure'''
        return self.tlv
    def getInterpretation():
        return self.interpretation

    def __str__(self):
        return self.title+":"+str(self.tlv)+":"+self.interpretation
    
if __name__ == "__main__":
    e1 = Element()
    e1.setTitle("1")
    e1.setValue(BerTlv("e1","1234"))
    e1.setInterpretation("this is e1")
    e2 = Element()
    e2.setTitle("2")
    e2.setValue(BerTlv("e2","3456"))
    e2.setInterpretation("this is e2")
    e3 = Element()
    e3.setTitle("3")
    e3.setValue(BerTlv("e3","5678"))
    e3.setInterpretation("this is e3")

    a = [e1, e2, e3]
    print(a)
    print(str(a[0]))
    print(str(a[1]))
    print(str(a[2]))
    
