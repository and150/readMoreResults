#-*- coding:utf-8 -*-
import constants as cts
import datetime
import time
from dateutil.relativedelta import relativedelta
from datescompare import date2days
from printrate import printRate


def getStartOilRate(ResArr, times, T, V, wi, i):
    startTrig = 0
    startOilRate = 0
    averOilRate = 0 # average oil rate for 1st year of production

    cumOil1 = 0
    time1 = 0
    period = 365

    cumOil = ResArr[T*V*wi + T*cts.i_d['Sopt'] + len(times)-1]

    for i in range(1, len(times)):

        if(startTrig==0 and ResArr[T*V*wi + T*cts.i_d['Sopr'] + i] >0):
            startTrig = 1
            startOilRate = ResArr[T*V*wi + T*cts.i_d['Sopr'] + i]  

        if(ResArr[T*V*wi + T*cts.i_d['Sopr'] + i-1] == 0 and  ResArr[T*V*wi + T*cts.i_d['Sopr'] + i] >0 ):
            cumOil1 = ResArr[T*V*wi + T*cts.i_d['Sopr'] + i]
            time1 = times[i].tos

        if(times[i].tos - time1 >= period):
            avRate = (ResArr[T*V*wi + T*cts.i_d['Sopt'] + i] - cumOil1) / (times[i].tos - time1) * 1000

    return [startOilRate, avRate, cumOil]



    ResArr[T*V*wi + T*cts.i_d['Sopt'] + i] 


# function prints information for cross-plots
def getAVRCUM(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    #cptOutFile = open(currDir+"\\"+rootName+".CPTout","w") # crossplot out file
    T = len(times) # number of rate-file records
    W = len(wellNames) # amount of wells
    MZ = numsArray[5-1] # amount of layers
    V = cts.VEC + MZ*2*numsArray[55-1]       # amount of vectors



    for x in wellNames:
        wi = (wellNames.index(x))
        print(x, getStartOilRate(ResArr, times, T, V, wi, i))


    #cptOutFile.close()


