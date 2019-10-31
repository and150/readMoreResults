#-*- coding:utf-8 -*-
import constants as cts
import datetime
import time
from datescompare import *

#################### IT utilities ###########################
class WTItem:
    def __init__(self, well="", start = 0.0, stop = 0.0, wt = 0):    
        self.well = well     # well name
        self.wt = wt         # wt number
        self.start = start   # well test start
        self.stop = stop    # well test end  
        
    def printList(self):
        print(self.well, self.start, self.stop, self.wt)  


def GetITlist(filename, SDAT): 
    ITLIST = []
    lines = [line.rstrip('\n') for line in open (filename)] 
    for x in lines:
        if len(x)>0: 
            words = x.split()
            ITLIST.append( WTItem( words[0],  date2days(words[1]+" "+words[2], SDAT), date2days(words[3]+" "+words[4], SDAT), words[5] ))
            #print (words[1]+" "+words[2]," | ", words[3]+" "+words[4])
    return ITLIST
 

# get graphs of pressure for interference tests
def getIT(currDir, rootName, startDate, times, numsArray, RateOut):

    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()


    wtFileName   = currDir+"\\"+rootName+".ITlist"  # well test list input file name
    outFile  = open(currDir+"\\"+rootName+".ITgraphs", "w") # graphs output

    ### interference test list processing
    WTlist = GetITlist(wtFileName, startDate)  #gets welltest list (must be sorted)
      

    ## get well index in Item array
    tr = 0
    timetol = cts.TIMETOL
    liqCut = cts.LIQCUT
    PBUstr = ""
    T = len(times) # amount of RATE-file entries
    W = len(wellNames) # wells number
    MZ = numsArray[5-1] #  number of connections
    V = cts.VEC + MZ*2*numsArray[55-1]       # number of vectors


    for x in WTlist: # for all wells and tests
        PBUstr = ""
        wi = (wellNames.index(x.well))     
        #print(x.wt.split('_'))
        wi_disturb = (wellNames.index(x.wt.split('_')[1]))
        for i in range(0,T): # for all times of RATE-file
            # output only within welltest period
            if(times[i].tos >= x.start and times[i].tos <= x.stop):             
            #if(x.start - times[i].tos < timetol and times[i].tos - x.stop < timetol):                
                # output to *.WTgraphs  no filters
                outFile.write("\n")
                outFile.write("IT=" + str(x.wt)+ " ")                            # test number
                outStr = str(times[i].tos) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # time and well name

                outFile.write(str(ResArr[T*V*wi + T* cts.Sbhp + i])); outFile.write(" ")  # simulated BHP
                outFile.write(str(ResArr[T*V*wi + T* cts.Sopr + i])); outFile.write(" ")  # simulatdd oil rate
                outFile.write(str(ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i])); outFile.write(" ")  # simulated water rate (injection)

                outFile.write(str(ResArr[T*V*wi + T* cts.Hbhp + i])); outFile.write(" ")  # historic BHP
                outFile.write(str(ResArr[T*V*wi + T* cts.Hopr + i])); outFile.write(" ")  # historic oil rate
                outFile.write(str(ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i])); outFile.write(" ")  # historic water rate + injection

                outFile.write(str(ResArr[T*V*wi_disturb + T* cts.Hwpr + i] + ResArr[T*V*wi_disturb + T* cts.Hwir + i]))   # injection of disturbing well 
                
    outFile.close()
