#-*- coding:utf-8 -*-
import constants as cts
from item_class import *

# get graphs of pressure for interference tests
def getIT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    wtFileName   = currDir+"\\"+rootName+".ITlist"          # well test list input file name
    outFile  = open(currDir+"\\"+rootName+".ITgraphs", "w") # graphs output

    ### interference test list processing
    WTlist = test_items()
    WTlist.get_items_list(wtFileName, startDate)
      
    T = len(times)                      # amount of RATE-file entries
    MZ = numsArray[5-1]                 # number of connections
    V = cts.VEC + MZ*2*numsArray[55-1]  # number of vectors

    for x in WTlist.items_list: # for all wells and tests
        wi = (wellNames.index(x.well))     
        wi_disturb = (wellNames.index(x.wt.split('_')[1])) # splitter for "WellTest_DisturbingWell" entry
        for i in range(0,T): # for all times of RATE-file
            # output only within welltest period
            if(times[i].tos >= x.start and times[i].tos <= x.stop):             
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
