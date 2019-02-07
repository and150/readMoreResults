import constants as cst
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
    V = cst.VEC + MZ*2*numsArray[55-1]       # количество векторов 
    #indexes of vectors
    Sopr  = cst.Sopr
    Swpr  = cst.Swpr 
    Sbhp  = cst.Sbhp
            
    Sopt  = cst.Sopt  
    Swpt  = cst.Swpt  
    Swit  = cst.Swit  

    Hopr  = cst.Hopr  
    Hwpr  = cst.Hwpr  
    Hbhp  = cst.Hbhp  
    Hwefa = cst.Hwefa 


    #t0 = date2days("01.10.2018 00:00:00", startDate)
    #t1 = date2days("01.11.2018 00:00:00", startDate)
    printRate(times, numsArray, RateOut)




