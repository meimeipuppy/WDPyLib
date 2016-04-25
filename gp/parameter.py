#parameter.py
#@Class LoadParam InstallParam
#@Author: mei yang
#@Creation: March-5-2014
from construct.berlv import *
from construct.berlvs import *
from construct.bertlv import *
from construct.mixtlvs import *

#install
TAG_AppSpecParam = "C9" # application specific parameters
#load&install
TAG_SystemSpecific = "EF"
    TAG_NonVolatileCodeMemory = "C6"      #load
    TAG_VolatileDataMemory = "C7"         #load&install
    TAG_NonVolatileDataMemory = "C8"      #load&install
    TAG_GlobalService = "CB"              #install
    TAG_LoadFileDataBlockFormatID = "CD"  #load
    TAG_VolatileRsvdMemory = "D7"         #install
    TAG_NonVolatileRsvdMemory = "D8"      #install
    TAG_TS102226 = "CA"                   #install
    TAG_ImplicitSelect = "CF"             #install
    TAG_LoadFileDataBlockParam = "DD"     #load
#install
TAG_TS102226Templ = "EA" # TS102.226 specific template
#load&install
TAG_CFT = "B6" # ControlReferenceTemplate
    #all subTags shared by load&install
    TAG_IdNumber = "42" # Identification Number of the security
                        # domain with the token verification privilege
    TAG_ImageNumber = "45"
    TAG_APId = "5F20"   # application provider id
    TAG_TokenId = "93"
    

class LoadParam():
    '''load parameters, all get function will return a map structure, key is the BerTlv, value is the meaning
        of the value
    '''
    def __init__(self, *args):
        if(len(args)==1): #has string
            self.data = args[0]  #string
            tlvs = BerTlvs(self.data)
            #first level tlv
            self.sysSpecificTlvs = BerTlvs(tlvs.findTlv("TAG_SystemSpecific").getValue())
            self.ctrlRefTlvs = MixTlvs(tlvs.findTlv("TAG_CFT").getValue(), ['5F20'])

        # empty construction - todo

    def __getSysSpecParam(self):
        '''return BerTlv of system specific parameters'''
        return self.sysSpecificTlvs

    def __getCtrlRefTemplte(self):
        return self.ctrlRefTlvs

    def __getNonVolCodeMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_NonVolatileCodeMemory")
    def __getVolDataMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_VolatileDataMemory")
    def __getNonVolDataMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_NonVolatileDataMemory")
    def __getLoadFileDataBlkForm(self):
        return self.sysSpecificTlvs.findTlv("TAG_LoadFileDataBlockFormatID")
    def __getLoadFileDataBlkParam(self):
        return self.sysSpecificTlvs.findTlv("TAG_LoadFileDataBlockParam")
    def __getIdNum(self):
        return self.ctrlRefTlvs.findTlv("TAG_IdNumber")
    def __getImgNum(self):
        return self.ctrlRefTlvs.findTlv("TAG_ImageNumber")
    def __getApId(self):
        return self.ctrlRefTlvs.findTlv("TAG_APId")
    def __getTokenId(self):
        return self.ctrlRefTlvs.findTlv("TAG_TokenId")

class InstallParam():
     '''install parameters, all get function will return a map structure, key is the BerTlv, value is the meaning
        of the value
     '''
    def __init__(self, *args):
        if(len(args)==1): #has string
            self.data = args[0]  #string
            tlvs = BerTlvs(self.data)
            #first level tlv
            self.appSpecParamTlvs = BerTlvs(tlvs.findTlv("TAG_AppSpecParam").getValue())
            self.sysSpecificTlvs = BerTlvs(tlvs.findTlv("TAG_SystemSpecific").getValue())
            self.ctrlRefTlvs = MixTlvs(tlvs.findTlv("TAG_CFT").getValue(), ['5F20'])
    def __getAppSpecParam(self):
        return self.appSpecParamTlvs
        
    def __getSysSpecParam(self):
        '''return BerTlv of system specific parameters'''
        return self.sysSpecificTlvs

    def __getCtrlRefTemplte(self):
        return self.ctrlRefTlvs

    def __getNonVolCodeMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_NonVolatileCodeMemory")
    def __getVolDataMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_VolatileDataMemory")
    def __getNonVolDataMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_NonVolatileDataMemory")
    def __getGlobalService(self):
        return self.sysSpecificTlvs.findTlv("TAG_GlobalService")
    def __getLoadFileDataBlkForm(self):
        return self.sysSpecificTlvs.findTlv("TAG_LoadFileDataBlockFormatID")
    def __getVolatileRsvdMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_VolatileRsvdMemory")
    def __getNonVolatileRsvdMem(self):
        return self.sysSpecificTlvs.findTlv("TAG_NonVolatileRsvdMemory")
    def __getTS102226(self):
        return self.sysSpecificTlvs.findTlv("TAG_TS102226")
    def __getImplicitSelect(self):
        return self.sysSpecificTlvs.findTlv("TAG_ImplicitSelect")
    def __getLoadFileDataBlkParam(self):
        return self.sysSpecificTlvs.findTlv("TAG_LoadFileDataBlockParam")
    def __getIdNum(self):
        return self.ctrlRefTlvs.findTlv("TAG_IdNumber")
    def __getImgNum(self):
        return self.ctrlRefTlvs.findTlv("TAG_ImageNumber")
    def __getApId(self):
        return self.ctrlRefTlvs.findTlv("TAG_APId")
    def __getTokenId(self):
        return self.ctrlRefTlvs.findTlv("TAG_TokenId")
