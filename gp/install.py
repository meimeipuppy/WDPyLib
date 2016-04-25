#install.py
#@Class Install
#@Author: mei yang
#@Creation: Feb-26-2014
from construct.berlv import *
from construct.berlvs import *
from construct.bertlv import *
from parameter import *

class Install(APDU):

    #constants:
    MASK_P1_ONECMD = 0
    MASK_P1_MORECMD = 0x80
    MASK_P1_REGUPDATE = 0x40
    MASK_P1_PERSO = 0x20
    MASK_P1_EXTRADITION = 0x10
    MASK_P1_MAKESELECTABLE = 8
    MASK_P1_INSTALL = 4
    MASK_P1_LOAD = 2
    
    P2_NOINFO = 0
    P2_BEGIN = 1  # beginning of combined load,install and make selectable
    P2_END = 3    # end of combined ...





class InstallDataLoad():
    '''construct of install data field'''
    def __init__(self, *args):
        '''InstallData() or InstallData(String)'''
        if(len(args)==0): #empty
            self.loadFileAid = BerLv(value="") 
            self.securityDomainAid = BerLv(value="")
            self.loadFileBlockHash = BerLv(value="")
            self.loadParameters = BerLv(value="")
            self.loadToken = BerLv(value="")

            
        else:#has data
            data = args[0] #install_data
            lvs = BerLvs(data)
            self.loadFileAid = lvs.findLv(1)
            self.securityDomainAid = lvs.findLv(2)
            self.loadFileBlockHash = lvs.findLv(3)
            self.loadParameters = lvs.findLv(4)
            self.loadToken = lvs.findLv(5)
    #getter:
    def getLoadFileAid(self):
        return self.loadFileAid.getData()
    def getSecurityDomainAid(self):
        return self.securityDomainAid().getData()
    def getloadFileBlockHash(self):
        return self.loadFileBlockHash.getData()
    def getLoadParameters(self):
        return self.loadParameters.getData()
    def getLoadToken(self):
        return self.loadToken.getData()
    #setter:
    def setLoadFileAid(self, aid):
        self.loadFileAid.setData(aid)
    def setSecurityDomainAid(self, aid):
        self.securityDomainAid.setData(aid)
    def setLoadFileBlockHash(self, blockHash):
        self.loadFileBlockHash.setData(blockHash)
    def setLoadParameters(self, param):
        self.loadParameters.setData(param)
    def setLoadToken(self, token):
        self.loadToken.setData(token)

    #Representation:
    def __str__(self):
        return str(self.loadFileAid)+str(self.securityDomainAid)\
                        + str(self.loadFileBlockHash) + str(self.loadParameters)\
                        + str(self.loadToken)
    #Semantics
    def getDict(self):
        dict d
        d.append()
            
            
    
