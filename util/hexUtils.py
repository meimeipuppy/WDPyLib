#hexUtils.py


def intToHexByteStr(intNumber):
    '''from int to hex byte string in upper letter;
        for example, '6'->'06','480'->'0x01E0'
    '''
    if(len(hex(intNumber))%2!=0):
        return '0{0:X}'.format(intNumber)
    else:
        return '{0:X}'.format(intNumber)


def asciiToString(ascstring, spacing=""):
    '''
        ascii string to its character representation,
         - with spacing, default none
        e.g. "3334356162" -> "345ab"
    '''
    l = len(ascstring)
    off = 0
    result = ""
    while(off<l):
        result = result + chr(int(ascstring[off:off+2],16))
        if(off!=l-2):
            result = result + spacing
        off = off+2
    return result

def hexStringToIpString(string):
    '''
        "3e9fab781d" -> "62.159.171.120"
    '''
    l = len(string)
    off = 0
    result = ""
    while(off<l):
        result = result + str(int(string[off:off+2], 16))
        if(off!=l-2):
            result = result + "."
        off = off + 2
    return result

def xorString(str1, str2):
    '''
        str1 ^ str2 (char by char)
    '''
    if(len(str1)!=len(str2)):
        raise ValueError("length of strings are not the same.")
    strLength = len(str1)
    off = 0
    result = ""
    while(off<strLength):
        result = result + chr((ord(str1[off:off+1]) ^ ord(str2[off:off+1])))
        off = off + 1
    return result

if __name__ == "__main__":
    print(intToHexByteStr(1)) #01
    print(intToHexByteStr(32)) #20
    print(intToHexByteStr(480)) #01E0


    s = "3132333435363738"
    print(asciiToString(s))

    s1 = "\x3F\x01\x87\xAB\x9D\x3A"
    s2 = "\x33\xff\xf9\x01\x99\xbb"
    print(xorString(s1,s2).encode('hex'))



