#

def hlen(hexstring):
    return len(hexstring)/2


def tobin(hexstring):
    '''turn '02E3' to '0000001011100011' '''
    ints = int(hexstring,16)
    binlen = len(hexstring)*4
    #print(str(ints))
    bins = str(bin(ints)) # here has 0b, and lose the leading 0s
    #print(bins)
    return pad_leading0(bins[2:],binlen)

def pad_leading0(string, tlen):
    if(len(string)==tlen):
        return string
    else:
        while(len(string)<tlen):
            string = "0"+string
        return string

    
if __name__ == "__main__":
    print(str(hlen("0102030405060708")))
    
    print(tobin("0011224E"))
