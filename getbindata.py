#-*- coding:utf-8 -*-
#import struct
import array

def getBinData(input_file, input_type='char',amount=1,pr=0): 
    bytes_length = {'int':4, 'float':4, 'char':1}
    types = {'int':'l', 'float':'f', 'char':'b'}

    arr = array.array(types[input_type])
    arr.frombytes(input_file.read(amount*bytes_length[input_type]))

    if input_type is 'char': 
        arr = array.array.tobytes(arr).decode('utf-8')

    if pr== 1: print(arr)
    if amount > 1: 
        return arr
    else:
        return arr[0]



'''
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
'''


