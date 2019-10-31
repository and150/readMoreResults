#-*- coding:utf-8 -*-
import constants as cts
import datetime
import time
from datescompare import *

#################### PLT output functions #######################
class WTItem:
    def __init__(self, pltInts, well="", start = 0.0, stop = 0.0, wt = 0  ):    
        self.well = well     # well name
        self.wt = wt         # wt number
        self.start = start   # well test start
        self.stop = stop    # well test end  
        self.pltInts = pltInts   # well PLTintervals array
    def printList(self):
        print(self.well, self.start, self.stop, self.wt, self.pltInts)  


def GetPLTlist(filename, SDAT):
    PLTLIST = []
    lines = [line.rstrip('\n') for line in open (filename)] 
    for x in lines:
        if len(x)>0: 
            words = x.split()
            PLTLIST.append(  WTItem( words[3:],  words[0], date2days(words[1]+" "+words[2], SDAT) )   )
    return PLTLIST

def printPlt(pltItem, pltarr, pltLR, times, wellNames, tstep, wnumb, pltOutFile):

    pltOutFile.write( '{} {} '.format( times[tstep].tos, wellNames[wnumb]) ) 
    #print( '{} {} '.format( times[tstep].tos, wellNames[wnumb]), end = '') # console output 

    s = 0
    f = s
    for i in range(0, len(pltItem.pltInts)):
        f = int(pltItem.pltInts[i])

        pltOutFile.write( '{:.3f} '.format(sum(pltarr[s:f])/pltLR ))                    
        #print( '{:.3f} '.format(sum(pltarr[s:f])/pltLR ), end = '') # console output
        #print( '|{:d} {:d}| '.format(s,f ), end = '') # debug console output
        s = f

    pltOutFile.write('\n')
    #print()  # console output




def getPLT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()



    pltFileName = currDir+"\\"+rootName+".PLTlist"  # input PLT list
    pltOutFile = open(currDir+"\\"+rootName+".PLTout","w") # PLT out file

    MZ = numsArray[5-1] # number of layers
    T = len(times) # rate file records number
    W = len(wellNames) # wells amount
    V = cts.VEC + MZ*2*numsArray[55-1]      # vectors amount 
    Vbase = cts.VEC

    # read PLT
    PLTlist = []       
    PLTlist = GetPLTlist(pltFileName,startDate)
    #for p in PLTlist:
    #    print(p.well, days2date(p.start, startDate), p.pltInts)


    for x in PLTlist: # for all wells and PLTs
        j = (wellNames.index(x.well))     
        #print(x.well, x.wt, x.start, days2date(x.start, startDate)) # debug

        for i in range(0,len(times)):
            #print(x.well, times[i].tos, days2date(times[i].tos, startDate), x.start, days2date(x.start, startDate)) # debug
            #if(times[i].tos == x.start): 

            if(abs(times[i].tos - x.start) <= cts.TIMETOL+ 0.001): 
                pltarr = [0]*MZ 
                for k in range(0,MZ):
                    #print("{:.3f}".format(ResArr[T*V*j + T*(Vbase+k) + i] + ResArr[T*V*j + T*(Vbase+MZ+k) + i]), end=" ")    # debug out
                    # temporaty PLT-vector for every timestep for every well                   
                    pltarr[k] = ResArr[T*V*j + T*(Vbase+k) + i] + ResArr[T*V*j + T*(Vbase+MZ+k) + i] 

                # console out
                #print(pltarr)
                #print(sum(pltarr[0:4]), sum(pltarr[4:7]) ,sum(pltarr[7:10]), end = " ") # 
                #print(sum(pltarr[0:34]), sum(pltarr[34:56]), sum(pltarr[56:66]), sum(pltarr[66:75]), sum(pltarr[75:89]), end = " ") # 
                #print()  

                # print to file
                pltLR = sum(pltarr) 
                if pltLR != 0: 
                    printPlt(x, pltarr, pltLR, times, wellNames, i , j, pltOutFile)

                else:
                	pltOutFile.write( '{} {}  liquid_rate=0\n'.format( times[i].tos, wellNames[j] ) )                                    
