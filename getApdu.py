
# abstract apdu from log file provided by EZL singapore
# @version:v1
# @author: mei.yang
# @call: python getApdu.py d:\xxx\xxx\dkin.txt

from textify.apduTextifier import *

def printApdu(out, apduLine):
    apduLine = getapdu(apduLine)
    out.write(apduLine)
    out.write("\n")

def printMsg(out, msg):
    out.write(msg)
    out.write("\n")

def getapdu(msg):
    return msg.strip().replace(" ","").replace("sw","").replace("SW","")

    
def getApduFromFile(file):
    with open(file, "r") as logfile:
        outfile = open(file+ '_apdu.txt', "w")
        for line in logfile:
            printApdu(outfile, line) #print apdu first
            if line.startswith("80"):
                sapdu = getapdu(line)
                #print("apduline="+sapdu)
                tf = ApduTextifier(sapdu)
                text = tf.textify()
                #print("info="+text)
                if(text!=None):
                    printMsg(outfile, text)
                
    logfile.close()
    outfile.close()



if __name__ == "__main__":
    import sys
    #print(sys.argv[1])
    getApduFromFile(sys.argv[1])
    print("done")
