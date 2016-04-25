#hash

import hashlib
import hmac
from util.hexUtils import *

class TlsPrf():

    '''
    do 
    PRF(secret, label, seed) = P_MD5(S1, label + seed) XOR
                                  P_SHA-1(S2, label + seed);
    for TSL protocol
    '''
    def __init__(self, *args, **kwargs):
        '''
        TlsPrf(secret="",label="",seed="")
        secret/seed accepts only hex string like '7f3e019abb8023cd' (will be converted)
        label accepts ascii string like 'this is a string'
        '''
        if(kwargs!={}):
            if(kwargs["secret"]!=None):
                #convert input key from '7f3e019abb8023cd..'-> 'x7f\x3e\x01\x9a\xbb..'
                self.secret = kwargs["secret"].decode('hex')
                keylen = len(self.secret)
                if(keylen%2!=0):
                    raise ValueError("key len is odd")
                #infact, should support odd length key
                #round-up rule for s2: first byte of s2 is last byte of s1
                self.S1 = self.secret[0:keylen/2]
                self.S2 = self.secret[keylen/2:keylen]
            if(kwargs["label"]!=None):
                self.label = kwargs["label"]
            if(kwargs["seed"]!=None):
                self.seed = kwargs["seed"].decode('hex')
            #self.hash

    def setSeed(self, seed):
        self.seed = seed

    def p_hash(self, bytes2expand, func_name):
        '''
            @bytes2expand: number of bytes to expand the message hash
            @func_name: "md5"(P_MD5) or "sha1" (P_SHA1)
            @return: digest (not hex)
            p_hash(secret, seed) = HMAC_hash(secret, A(1)+seed)+\
                HMAC_hash(secret, A(2)+seed) + \
                HMAC_hash(secret, A(3)+seed) + \

            A() is defined as:
            A(0) = seed
            A(i) = HMAC_hash(secret, A(i-1))

            HMAC_hash -> hmac (python)

            for hash lib python commands update & digest()
            update('1234')
            digest()
            update('5678')
            digest()
            =
            update('12345678')
            digest()
        '''
        hashlen = 0;
        if(func_name=="md5"):
            #func = getattr(hashlib, 'md5') #func() = hashlib.md5()
            func = hashlib.md5
            hashlen = 16
            key = self.S1
        elif(func_name=="sha1"):
            #func = getattr(hashlib, 'sha1')#func() = hashlib.sha1()
            func = hashlib.sha1
            hashlen = 20
            key = self.S2
        
        #hashmode = func() #create instance of the hash object
        hashmode = func

        print(hashmode)
        
        remainder = bytes2expand % hashlen
        x = bytes2expand / hashlen # x rounds
        if(remainder!=0):
            x = x+1    #64/20 = 3 80/20=4

        #generate p_hash
        #HMAC_hash = hmac.new(key, msg=None, digestmod = hashmode)
        seed = self.label + self.seed
        digest = ""
        ax = seed
        for n in range(0, x):
            #calculate A(x)
            HMAC_hash = hmac.new(key, msg=ax, digestmod = hashmode)
            #HMAC_hash.update(ax)
            ax = HMAC_hash.digest()
            #calculate p_hash
            HMAC_hash = hmac.new(key, msg=(ax+seed), digestmod = hashmode)
            #HMAC_hash.update(ax + seed)
            digest = digest + HMAC_hash.digest() # digest = p_hash

        return digest[:bytes2expand] #.encode('hex') # encode: to hex digest
        
        
if __name__ == "__main__":

    #calculate master key
    #master_secret = PRF(pre_master_secret, "master secret",
    #   ClientHello.random + ServerHello.random) [0..47]
    tlsPrf = TlsPrf(secret="00100000000000000000000000000000000000100123456789ABCDEFFEDCBA9876543210",\
                    label="master secret",\
                    seed="9B660E0BA9F8E6FBA9E815AF7DA58C9F1943BAE1768B6210AB14992B749613358D576D4E7E4BA72EBCF3D2C4739FAD683C10EEC5C76AA93A816020ABBC132204")
    
    p_md5 = tlsPrf.p_hash(48, "md5")
    p_sha1 = tlsPrf.p_hash(48, "sha1")
    master_secret = xorString(p_md5, p_sha1)
    print("master_secret is:" + master_secret.encode('hex'))
    
    #calculate finished message
    #verify_data
    # PRF(master_secret, finished_label, MD5(handshake_messages) +
    # SHA-1(handshake_messages)) [0..11];
    

