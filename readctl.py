#-*- coding:utf-8 -*-
import struct
from getbindata import getBinData


def readCTL(input_file):
    
    class CTLline:
    #local class for lines of CTL input_file    
       def __init__(self, tsn=0, wfa=0, wfr=0, tos=0, stl=0, plns=0):    
           self.tsn = tsn # time step number
           self.wfa = wfa # write flag for array (1 - written)  
           self.wfr = wfr # write flag for rate (1 -written)
           self.tos = tos # time of the step
           self.stl = stl # step length
           self.plns= plns # projected lenght of next step
      
       def getData(self, line):
           self.tsn = struct.unpack('i',line[0:4])[0] #int.from_bytes(line[0:4],'little')
           self.wfa = struct.unpack('i',line[4:8])[0] #int.from_bytes(line[4:8],'little')   
           self.wfr = struct.unpack('i',line[8:12])[0] #int.from_bytes(line[8:12],'little') 
           self.tos = struct.unpack('f',line[12:16])[0] #struct.unpack('f',line[12:16])[0]
           self.stl = struct.unpack('f',line[16:20])[0] #struct.unpack('f',line[16:20])[0]
           self.plns= struct.unpack('f',line[20:24])[0] #struct.unpack('f',line[20:24])[0]
   
       def printCTLline(self):
           print(self.tsn, self.wfa, self.wfr, self.tos, self.stl, self.plns)
 

    #read CTL file
    method = getBinData(input_file,'int',1,)  #XXX
    ni = getBinData(input_file,'int',1,)      # number of integers in each record
    nf = getBinData(input_file,'int',1,)      # number of float in each record

    line = ""
    ARR = []
    #ctl = {}
    ctl = {'tsn':[], 'wfa':[], 'wfr':[], 'tos':[], 'stl':[], 'plns':[]}

    rateNum = 0 # rate records counter
    while True:        
        line=input_file.read(ni*4+nf*4)
        if not line: break
    
        a = CTLline()
        a.getData(line)
        ctl['tsn'].append(a.tsn)
        ctl['wfa'].append(a.wfa)
        ctl['wfr'].append(a.wfr)
        ctl['tos'].append(a.tos)
        ctl['stl'].append(a.stl)
        ctl['plns'].append(a.plns)
        #a.printCTLline()
        ARR.append(a)
        del a

    times = []        
    for i in range(0,len(ARR)):    #counts number of rate records
        rateNum+=ARR[i].wfr    
        if ARR[i].wfr == 1:  
            times.append(ARR[i])
            # debug output
            #print(ARR[i].tsn, ARR[i].wfa, ARR[i].wfr, ARR[i].tos, ARR[i].stl, ARR[i].plns, )
    

    #print(ctl)
    # TODO change times to ctl (without filtering for more universal approach) 
    # TODO times is currently filtered array!!! (only rate timesteps)
    #for k, v in ctl.items(): print(k,v)
    #print()
    #for i in times: print(i.tsn, i.wfr)
    #print()

    return (times, ctl)
