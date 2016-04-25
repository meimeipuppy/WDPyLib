#@Class ApduTextifier
#@Author: mei yang
#@Creation: Feb-26-2016

from construct.bertlv import *
from construct.bertlvs import *
from util.hexUtils import *
from iso.apdu import *
from tagsConstants import *

class ApduTextifier():
    '''
    Texity APDU strings.
    interprete apdu meanings.
    Proactive Command
    ..

    '''

    def __init__(self, *args):
        '''
        ApduTextify(string apdu);
        '''
        self.apdu = APDU(args[0])
    

    def textify(self):
        return self.getCmdDetails()


    def getCmdDetails(self):
        if(self.apdu==None):
            return "NO APDU"
        else:
            cmdType = self.apdu.getIns();
            if(cmdType == TAGS.INS_FETCH):
                return "ProactiveCommand: " + self.getProactiveCmdDetails()
            elif(cmdType == TAGS.INS_TR):
                return "TerminalResponse: " + self.getProactiveResponseDetails()
            else:
                return None


    def getProactiveCmdDetails(self):
        #print("getProactiveCmdDetails")
        d0data = self.apdu.getData()
        firstbyte = int(d0data[0:2],16)
        if(firstbyte==self.apdu.getIns()):
            d0data = self.apdu.getData()[2:] #remove ins in transmitted log
        
        d0tlv = BerTlv(d0data, taglen=1) # d0 L v
        data = d0tlv.getValue() #string
        details = self.getTagDetails(data)
        if(details==None):
            return ""
        else:
            #print("detaoils="+details)
            return details 

    def getProactiveResponseDetails(self):
        respdata = self.apdu.getData()
        firstbyte = int(respdata[0:2],16)
        if(firstbyte==self.apdu.getIns()):
            respdata = self.apdu.getData()[2:] #remove ins in transmitted log
        details = self.getTagDetails(respdata)
        if(details==None):
            return ""
        else:
            return details 

    def getTagDetails(self, data):
        '''data: string, this data is a tertlvs '''
        offset = 0
        alltags = BerTlvs(data) # first layer bertlvs
        #1define command type first
        #1.1 find cmd detail tag
        cmdtlv = self.findTAG(TAGS.TAG_CMD_DETAIL, alltags)
        if(cmdtlv == None):
            return "PARSING ERROR(NO COMMAND DETAIL)"
        else:          
            #1.2 parse cmd type, 2nd byte in cmd_detail tlv
            cmdType = int( cmdtlv.getValue()[2:4],16 ) #int the cmdType
            #print("cmdtype:"+str(cmdType))
            #print(cmdType==0x40)
            if(cmdType == TAGS.PCMD_OPEN_CHANNEL):
                return "<cmd:OpenChannel>" + self.getChannelDetails(alltags)
            elif(cmdType == TAGS.PCMD_CLOSE_CHANNEL):
                return "<cmd:CloseChannel>" + self.getChannelDetails(alltags)
            elif(cmdType == TAGS.PCMD_RECEIVE_DATA):
                return "<cmd:ReceiveData>" + self.getDataDetails(alltags)
            elif(cmdType == TAGS.PCMD_SEND_DATA):
                return "<cmd:SendData>" + self.getDataDetails(alltags)
            else:
                return ""

    def getChannelDetails(self, tlvs):
        '''channel details'''
        details = ""
        details = details + \
                  self.findTagAndGetDetail(TAGS.TAG_ALPHA_ID, \
                                           tlvs, "alpha",  1)
        details = details + \
                  self.findTagAndGetDetail(TAGS.TAG_BEARER_DESCRIPTION, \
                                           tlvs, "bearer",  0)
        details = details + \
                  self.findTagAndGetDetail(TAGS.TAG_BUFFER_SIZE, \
                                           tlvs, "bufferSize",  0)
        #get port
        utitl = self.findTAG(TAGS.TAG_UICC_TERMINAL_ITL, tlvs)
        title = "Uicc/TerminalTransporLevel"
        if(utitl!=None and utitl.getLength()!=0):
            transType = utitl.getValue()[0:2] #first byte is the type
            i_tType = int(transType,16)
            sType = ""
            if(i_tType==1):
                sType = "UDP/UICCclient/Remote"
            elif(i_tType== 2):
                sType = "TCP/UICCclient/Remote"
            elif(i_tType ==3):
                sType = "TCP/UICCserver/Remote"
            elif(i_tType ==4):
                sType = "UDP/UICCclient/Local"
            elif(i_tType==5):
                sType = "TCP/UICCclient/Local"
            elif(i_tType==6):
                sType = "direct"
            else:
                sType = "unknown"
            port = str(int(utitl.getValue()[2:], 16))
            details = details + "<"+ title + ":"\
                      + sType + ":" + "Port=" + port + ">"
            
        #get address
        otherAddress = self.findTAG(TAGS.TAG_OTHER_ADDRESS, tlvs)
        title = "OtherAddress"
        if(otherAddress!=None):
            if(otherAddress.getLength()==0):
                details = details + "<"+title+":" + "null local address"+">"
            else:
                oa = otherAddress.getValue()
                aType = oa[0:2]
                i_aType = int(aType,16)
                if(i_aType==0x21):
                    s_aType = "IPv4 Address"
                if(i_aType==0x57):
                    s_aType = "IPv6 Address"
                ip = hexStringToIpString(oa[2:])
                details = details + "<" + title + ":" + s_aType \
                          + ":" + ip +">"
           
        return details

    def getDataDetails(self, tlvs):
        ''' receive/send data details '''
        details = ""
        #cdata=channeldata
        cData = self.findTAG(TAGS.TAG_CHANNEL_DATA, tlvs)
        if(cData!=None):
            details = details+ "<ChannelData:"
            data = cData.getValue();
            offset = 0
            end = cData.getLength()*2
            while(offset<end):
                contentType = int(data[offset:offset+2],16)#first byte
                offset = offset+2
                if(contentType == 0x16):
                    #handshake:
                    #offset=2
                    res = self.getHandshakeDetails(data,offset, details)
                    offset = res[0]
                    details = res[1]
                elif(contentType==0x17):
                    #application_data
                    #offset=2
                    res = self.getApplicationDataDetails(data, offset, details)
                    offset = res[0]
                    details = res[1]
                elif(contentType==0x14):
                    #changecipherSpec
                    res = self.getChangeCipherSpecDetails(data, offset, details)
                    offset = res[0]
                    details = res[1]
                elif(contentType==0x15):
                    #alertprotocol
                    res = self.getAlertProtocolDetails(data, offset, details)
                    offset = res[0]
                    details = res[1]
                else:
                    details = "rawdata="+data[offset-2:end]
                    offset = end
                if(offset<end):
                    details = details + "||"
            details = details + ">"

        cData = self.findTAG(TAGS.TAG_CHANNEL_DATA_LENGTH, tlvs)
        if(cData!=None):
            slength = hex(int(cData.getValue(),16))
            details = details + "<ChannelDataLength=" + \
                          slength + ">"
            
                        
        return details
        
    def findTagAndGetDetail(self, tag, tlvs, title, valuetype):
        '''this function is to find tag in tlvs and return
            the title and value (depending on valuetype required)
            use it for general tlv element
            tag: int; title: string; valuetype: 0-string, 1-ascii, 2-int
        '''
        details = ""
        tlv = self.findTAG(tag, tlvs)
        if(tlv!=None):
            if(valuetype==1): #ascii
                value = "'"+asciiToString(tlv.getValue())+"'"
                #print("value="+value)
            elif(valuetype==2): #int
                value = str(int(tlv.getValue(),16))
            else: #strings
                value = tlv.getValue()
            details = details + "<" + title + ":"+ value + ">" 
        return details

    def findTAG(self, logtag, tlvs):
        '''return a tlv structure'''
        tlv = tlvs.findTlv(intToHexByteStr(logtag))
        if(tlv == None):
            tlv = tlvs.findTlv(intToHexByteStr(logtag | 0x80))
        if(tlv == None):
            return None
        else:
            return tlv


    def getHandshakeDetails(self, data, off, details):
        '''all msg accumulated into details
            return list[int-offset, string-details]

        '''
        protocolVer = data[off:off+4] # protocol version
        off = off+4
        if(protocolVer=="0303"):
            protocolVer = "protocolVer=TLS1.2"
        elif(protocolVer=="0301"):
            protocolVer = "protocolVer=TLS1.0"
        elif(protocolVer=="0302"):
            protocolVer = "protocolVer=TLS1.1"
        else:
            protocolVer = "protocolVer="+protocolVer
        details = details+ "handshake:"+ protocolVer + "|"
        length = int(data[off:off+4],16) # 2-byte length
        off = off+4 #skip handshake msg length
        hsType = data[off:off+2]
        if(hsType=="01"):
            shsType = "type=ClientHello"
        elif(hsType=="02"):
            shsType = "type=ServerHello"
        elif(hsType=="0E" or hsType=="0e"):
            shsType = "type=ServerHelloDone"
        elif(hsType=="10"):
            shsType = "type=clientKeyExchange"
        else:
            details = details + "typeUnknown:" + data[off:off+length*2]
            return [off+length*2,details]
        details = details+ shsType + "|"
        off = off+2
        
        msgLength = int(data[off:off+2*3],16) #3-byte length
        off = off+2*3
        if(msgLength==0):
            return [off,details+"handshakemessage=null"]
        if(hsType=="10"):
            #clientkey exchange follows different data structure
            pskid_len = int(data[off:off+4],16) #2-byte length
            off = off+4
            details = details + "pskidentify='"+ \
                      asciiToString(data[off:off+pskid_len*2]) + "'"
            off = off + pskid_len*2
            return [off, details]
        
        #protocolVersion
        protocolVer = data[off:off+4] #2-byte version
        off = off+4
        if(protocolVer=="0303"):
            protocolVer = "protocolVer=TLS1.2"
        elif(protocolVer=="0301"):
            protocolVer = "protocolVer=TLS1.0"
        elif(protocolVer=="0302"):
            protocolVer = "protocolVer=TLS1.1"
        else:
            protocolVer = "protocolVer="+protocolVer
        details = details+ protocolVer + "|"
        #Random
        randomlen = 32*2;
        random = data[off:off+randomlen]
        off = off +randomlen
        details = details + "random=" + random + "|"
        #sessionid
        len_sessionid = int(data[off: off+2],16)
        off = off+2;
        if(len_sessionid !=0):
            sessionid = data[off:off+len_sessionid*2]
            details = details + "sessionid="+sessionid + "|"
            off = off+len_sessionid*2
        if(hsType=="01"): # client has sets of suites;
            len_csuite = int(data[off:off+4],16)#2-byte cipher suite length
            off = off+4
            if(len_csuite!=0):
                allsuite = "CipherSuite="
                loff = off
                endoff = off + len_csuite*2
                while(loff<endoff):
                    suite = data[loff:loff+4]#each cipher suite is 2-byte
                    loff = loff + 4
                    allsuite = allsuite + suite + "|"
                details = details + allsuite
                off = off + len_csuite*2
        elif(hsType=="02"):#server has only one cipher method
            details = details + "CipherSuite="+data[off:off+4]+ "|"
            off = off+4
        #compressionMethods
        commlen = int(data[off:off+2],16) #1-byte len
        off = off+2
        if(commlen!=0):
            details = details + "compressionMethods=" \
                    + data[off:off+2] + "|"
            off = off+2
        else:
            details = details + "compressionMethod=null" + "|"

        #extension
        len_ext = int(data[off:off+4],16)
        off = off+4
        if(len_ext!=0):
            details = details + "extension=" + \
                      data[off:off+len_ext*2]
            off = off+len_ext*2
        #end
        return [off,details]

    def getApplicationDataDetails(self, data, off, msg):
        protocolVer = data[off:off+4] # 2-byte protocol version
        off = off+4
        msgLen = int(data[off:off+4],16) # 2-byte length
        off = off+4 #skip len
        endoff = off+msgLen*2
        msg = msg + "applicationData:"
        msg = msg + "rawdata="+data[off:endoff] 
        return [endoff,msg]

    def getChangeCipherSpecDetails(self, data, off, msg):
        protocolVer = data[off:off+4] # 2-byte protocol version
        off = off+4
        msgLen = int(data[off:off+4],16) # 2-byte length
        off = off+4 #skip len
        endoff = off+msgLen*2
        msg = msg + "changeCipherSpec:"
        msg = msg + "rawdata="+data[off:endoff] 
        return [endoff,msg]

    def getAlertProtocolDetails(self, data, off, msg):
        protocolVer = data[off:off+4] # 2-byte protocol version
        off = off+4
        msgLen = int(data[off:off+4],16) # 2-byte length
        off = off+4 #skip len
        endoff = off+msgLen*2
        msg = msg + "alertProtocol:"
        msg = msg + "rawdata="+data[off:endoff] 
        return [endoff,msg]
    
if __name__ == "__main__":
    print("testing")
    tf = ApduTextifier("801200002CD02A010301400302028182050C4F70656E204368616E6E656C3501033902058E3C030227BE3E0521CA98E02F")
    text = tf.textify()
    print(text)

    tf = ApduTextifier("8014000017010301400302028281830100B8028100B50103B902058E")
    text = tf.textify()
    print(text)

    tf = ApduTextifier("801200004ED04C8103014301820281213641160303003C010000380303AA43FAC410B6DABF952A1699E6D3AD1376061AA5E493DE2E1AA01C58964384DF00000A00AE008C008B00B0002C010000050001000101")
    text = tf.textify()
    print(text)

    tf = ApduTextifier("801400000F810301430102028281830100B701FF")
    text = tf.textify()
    print(text)

    tf = ApduTextifier("801200000ED00C810301420082028121370136")
    text = tf.textify()
    print(text)

    tf = ApduTextifier("8014000047810301420002028281830100B63616030100310200002D030174C122C4D08A003768630E479B1BCD2BC79C8528ABED635D37A5DD6BEC84967300008B0000050001000101B70100")
    text = tf.textify()
    print("1--"+text)

    tf = ApduTextifier("801400001A810301420002028281830100B60916030100040E000000B70100")
    text = tf.textify()
    print("2--"+text)

    tf = ApduTextifier("8012000070D06E8103014301820281213663160301002B10000027002538393632313135393331353135353733373136462F41303030303030313531303030303030140301000101160301002885A1DFDD1510C6ECE2C6824BBD57F925621CB0A19059EFB7B52AA2E27AE3482E3701469544F385F7")
    text = tf.textify()
    print("3--"+text)
    
    tf = ApduTextifier("8014000044810301420002028281830100B63314030100010116030100281D6FF48261C0EED4AA536D3CE3B69C7B07BEDF5DA135CDAE858D83A5A7E9D212AB2CBE00BF637D69B70100")
    text = tf.textify()
    print("4--"+text)
    
    #application data
    tf = ApduTextifier("80140000FF810301420002028281830100B681ED17030100F8AAE4976D418ADB3A8C46DB1B72920E88997503861AEE976BF39BB3D0FB4F476277DC59526EC107A179865A981C85FE920C227E3BF8FB83E0FAB36FE5C6FE01986FA1856E152D285E03446DB0EB655E1F6EC28D674E7F31A253F44377C1EB8C859D8A3B2C5938957E2BBC94154609E97AC8B1CD6A99B17EE47153F58F1C3865D58039EC0E3BBF119F487E64C610B56470E76686521CA34F6A1CB83699A5DE533615FE07299645490034003B272F7F456511FB7301BFE9FEF3BB11CFB05BF234953D5F81A5141C0C12BB97D74B4F2EB8DABA51BB587BBFBF2BA8BE24BB0E85C3CD5A6648B867D386E1B70110")
    text = tf.textify()
    print("5--"+text)

    #http data
    tf = ApduTextifier("801200002AD028810301430182028121361D1503010018F998A7ED2A731ACCF0BDA116F696DAF7F287C5D786CCFA8E")
    text = tf.textify()
    print("6--"+text)

    #closechannel
    tf = ApduTextifier("801200000BD009810301410082028121")
    text = tf.textify()
    print("7--"+text)

    tf = ApduTextifier("801400000C810301410002028281830100")
    text = tf.textify()
    print("8--"+text)
