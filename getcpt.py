import constants as cts
import datetime
import time
from datescompare import date2days
from printrate import printRate


# function gets date-time and returns timestep number or -1 if date-time not found
def getTimeStepNumber(times, startDate, stringDate="01.01.1900 00:00:00"):
    T = len(times)
    i = T - 1
    while(i>=0):
        if( abs(date2days(stringDate, startDate) - times[i].tos) < cts.TIMETOL):
            return i
        i = i - 1
    return -1


# function prints information for cross-plots
def getCPT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    cptOutFile = open(currDir+"\\"+rootName+".CPTout","w") # файл вывода кроссплотов 
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во ячеек по вертикали, нужно сюда передавать параметр
    V = cts.VEC + MZ*2*numsArray[55-1]       # количество векторов 


    with open("../testDateList","r") as dateList:
        for line in dateList:
            i = getTimeStepNumber(times, startDate, line.strip('\n'))
            if(i>=0):
                print('{0:s} - timestep={1:4d}  tos = {2:5.11f} '.format(line.strip('\n'), i, times[i].tos) ) 
            else:
                print("{0:s} - no such date".format(line.strip('\n')))


        

    dateList.close()





