import constants as cts
import datetime
import time
from datescompare import date2days
from printrate import printRate

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

#   t0 = date2days("01.04.2017 00:00:00", startDate)
#   t1 = date2days("19.06.2017 12:13:59", startDate)
#   i0 = -1
#   i1 = -1
#   print(t0, t1)
#   print(times[3].tos, times[6].tos)
#
#
#   i = T-1
#   while(i>0):
#       if(abs(times[i].tos - t0) < cts.TIMETOL):
#           i0 = i
#       elif(abs(times[i].tos - t1) < cts.TIMETOL):
#           i1 = i
#       if(i0 > 0 and i1 > 0): break
#
#       i-= 1
#
#   if(i0 < 0 and i1 < 0): 
#       print("no such timesteps")
#   else:
#       print("i0 =",i0,"i1 =", i1)
#   print("i0 =",i0,"i1 =", i1)
#
#
#
#   #printRate(times, numsArray, RateOut)

    i0 = 0
    tt = 0
    with open("../testDateList","r") as dateList:
        for line in dateList:
            t0 = date2days(line.strip('\n'), startDate)
            for i in range(0,T):
                #if( t0 == times[i].tos):
                if( abs(t0 - times[i].tos) < cts.TIMETOL):
                    i0 = i
                    tt = times[i].tos
                    break
                else:
                    i0 = -1
                    tt = -999
            print('{0:s} {1:5.11f} {2:5.11f} {3:5.3f} {4:4d}'.format(line.strip('\n'), t0, tt,  t0 - tt, i0) ) 
        

    dateList.close()





