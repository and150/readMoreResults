#-*- coding:utf-8 -*-
import constants as cts
import datetime
import time
from datescompare import *

#################### PBU utilities ###########################
class WTItem:
    def __init__(self, well="", start = 0.0, stop = 0.0, wt = 0):    
        self.well = well     # well name
        self.wt = wt         # wt number
        self.start = start   # well test start
        self.stop = stop    # well test end  

    def printList(self):
        print(self.well, self.start, self.stop, self.wt)  


def GetWTlist(filename, SDAT): 
    WTLIST = []
    lines = [line.rstrip('\n') for line in open (filename)] 
    for x in lines:
        if len(x)>0: 
            words = x.split()
            WTLIST.append(    WTItem( words[0]  ,  date2days(words[1]+" "+words[2], SDAT), date2days(words[3]+" "+words[4], SDAT) , words[5]  )                 )
            #print (words[1]+" "+words[2]," | ", words[3]+" "+words[4])
    return WTLIST
 

def getWT(currDir, rootName, startDate, times, numsArray, RateOut):

    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()


    wtFileName   = currDir+"\\"+rootName+".WTlist"  # well test list input file name
    outFile  = open(currDir+"\\"+rootName+".WTgraphs", "w") # graphs output
    wtOutFile = open(currDir+"\\"+rootName+".WTout","w") # parameters output
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # header

    ####### well test list processing #######
    WTlist = GetWTlist(wtFileName, startDate)  #gets welltest list (must be sorted)
      

    #### get well index in Item array
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
        for i in range(0,T): # for all times of RATE-file
            # output only within welltest period
            if(times[i].tos >= x.start and times[i].tos <= x.stop):             
            #if(x.start - times[i].tos < timetol and times[i].tos - x.stop < timetol):                
                # output to *.WTgraphs  no filters
                outFile.write("\n")
                outFile.write("WT=" + str(x.wt)+ " ")                            # test number
                outStr = str(times[i].tos) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # time and well name

                outFile.write(str(ResArr[T*V*wi + T* cts.Sbhp + i])); outFile.write(" ")  # simulated BHP
                outFile.write(str(ResArr[T*V*wi + T* cts.Sopr + i])); outFile.write(" ")  # simulatdd oil rate
                outFile.write(str(ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i])); outFile.write(" ")  # simulated water rate (injection)

                outFile.write(str(ResArr[T*V*wi + T* cts.Hbhp + i])); outFile.write(" ")  # historic BHP
                outFile.write(str(ResArr[T*V*wi + T* cts.Hopr + i])); outFile.write(" ")  # historic oil rate
                outFile.write(str(ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i])); outFile.write(" ")  # historic water rate + injection
                


                # get PBU and print parameters to *.WTout
                # PBU rates calculation
                currLiq  = ResArr[T*V*wi + T* cts.Sopr + i] + ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i]# current simulated liquid rate
                currLiqH = ResArr[T*V*wi + T* cts.Hopr + i] + ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i]# current historic liquid rate

                #currOil  = ResArr[T*V*wi + T* cts.Sopr + i] # current simulated oil rate
                #currOilH = ResArr[T*V*wi + T* cts.Hopr + i] # current actual oil rate

                currP  = ResArr[T*V*wi + T* cts.Sbhp + i]   # simulatde BHP
                currPH = ResArr[T*V*wi + T* cts.Hbhp + i]   # historic BHP
                maxP = currP
                maxPH = currPH
                if currP <= cts.PTOL or currPH <= cts.PTOL :
                    maxP = maxP
                    maxPH = maxPH
                else:
                    maxP = currP
                    maxPH = currPH


                if i<=len(times):  nextLiq = ResArr[T*V*wi + T* cts.Sopr + i+1] + ResArr[T*V*wi + T* cts.Swpr + i+1]+ ResArr[T*V*wi + T* cts.Swir + i+1] # next simulated liquid rate
                else: nextLiq = currLiq
    
                if(currLiq > liqCut):   # check intervals with non-zero rate
                    outFile.write(" dynamic") 
                    if(nextLiq <= liqCut):                          
                        PBUstr = PBUstr + x.well + " " + str(times[i].tos) # name of the well and PBU start time
                        PBUstr = PBUstr + " " + str(currLiq) + " " + str(currLiqH) # simulated and historic rates(injectivities) of liquid
                        ###PBUstr = PBUstr + " " + str(currOil) + " " + str(currOilH) # simulated and historic oil rates
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Sbhp + i]) # simulated BHP
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Hbhp + i])  # historic BHP
                else:
                    outFile.write(" static")                    
                    if(nextLiq > liqCut): 
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Sbhp + i])   #
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Hbhp + i])   #
                        #PBUstr = PBUstr + " " + str(maxP)   #
                        #PBUstr = PBUstr + " " + str(maxPH)   #
                        #PBUstr = PBUstr + " " + str(times[i].tos)  # 
                        break # stop cycle after the first PBU read
        #print(str(x.wt)," ", PBUstr) # console output
        PBUstr = PBUstr + " " + str(maxP)   # simulated reservoir pressure
        PBUstr = PBUstr + " " + str(maxPH)   # historic reservoir pressure
        PBUstr = PBUstr + " " + str(times[i].tos)  # PBU stop time


        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n")  # PBU parameters output
    outFile.close()
    wtOutFile.close()
