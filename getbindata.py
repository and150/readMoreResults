#-*- coding:utf-8 -*-
import struct

def getBinData(bts, type="int",size=1,pr=0):
#read binary data from file stream and return array of tuples
    ARRAY = [0]*size
    if (type=='int'):
       for i in range(0,size):
            ARRAY[i] =  struct.unpack('i',bts.read(4))[0]
    elif (type=='float'):
        for i in range(0,size):
            ARRAY[i] = struct.unpack('f',bts.read(4))[0]
    elif (type=='char'):
        for i in range(0,size):
            ARRAY[i]=  str(struct.unpack('c',bts.read(1))[0], 'utf-8')  #read 1 char
    elif (type=='char4'):
        for i in range(0,size):
            ARRAY[i]=  str(b''.join(struct.unpack('c'*4,bts.read(4))), 'utf-8')  #read word of 4 chars
    elif (type=='char16'):
        for i in range(0,size):
            ARRAY[i]= str(b''.join(struct.unpack('c'*16,bts.read(16))), 'utf-8') #read word of 16 chars
    else: return 0
    if(pr==1): print (ARRAY) #comment to stop printing array
    return (ARRAY)



