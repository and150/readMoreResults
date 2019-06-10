import constants as cts
import datetime
import time
from dateutil.relativedelta import relativedelta
from datescompare import date2days
from printrate import printRate


def printCptByDate(ResArr, times, T, V,  x, wi,  cptDate, i, outFile):
    outFile.write('{0:s} {1:5.2f} '.format(cptDate, times[i].tos))  # вывод даты и времени шага
    outFile.write('{0:s} '.format(x) ) # вывод имени скважины
    
    outFile.write('{0:3f} '.format(ResArr[T*V*wi + T*cts.Sopt + i]) )  # вывод расчетной накопленной добычи нефти
    outFile.write('{0:3f} '.format(ResArr[T*V*wi + T*cts.Hopt + i]) )  # вывод фактической накопленной добычи нефти

    outFile.write('{0:5.3f} '.format(ResArr[T*V*wi + T*cts.Swit + i]) )  # вывод расчетной накопленной закачки 
    outFile.write('{0:5.3f} '.format(ResArr[T*V*wi + T*cts.Hwit + i]) )  # вывод фактической накопленной закачки 

    outFile.write('{0:5.3f} '.format(ResArr[T*V*wi + T*cts.Swpt + i]) )  # вывод расчетной накопленной добычи воды 
    outFile.write('{0:5.3f} '.format(ResArr[T*V*wi + T*cts.Hwpt + i]) )  # вывод фактической накопленной добычи воды 

    outFile.write('{0:5.3f} '.format(ResArr[T*V*wi + T*cts.Sbhp + i]) )  # вывод расчетного забойного давления                
    outFile.write('{0:5.3f} '.format(ResArr[T*V*wi + T*cts.Hbhp + i]) )  # вывод фактического забойного давления                


# function gets date-time and returns timestep number or -1 if date-time not found
def getTimeStepNumber(times, startDate, stringDate="01.01.1900 00:00:00"):
    T = len(times)
    i = T - 1
    CptTime = date2days(stringDate, startDate)
    passedCptDate = False

    while(i>=0):
        if(CptTime >= times[i].tos): 
            passedCptDate = True

        if(abs(CptTime - times[i].tos) < cts.TIMETOL):
            return i
        elif(passedCptDate == True):
            if(abs(CptTime - times[i].tos) <= abs(CptTime - times[i-1].tos)):
                return i
            elif(i>0):
                return i - 1
        i = i - 1
    return -1


# function prints information for cross-plots
def getCPT(currDir, rootName, startDate, times, numsArray, RateOut, cptDate):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    cptOutFile = open(currDir+"\\"+rootName+".CPTout","w") # файл вывода кроссплотов 
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во ячеек по вертикали, нужно сюда передавать параметр
    V = cts.VEC + MZ*2*numsArray[55-1]       # количество векторов 


    # get date one (or more) month behind, number of months set in constants
    cptDate1 = datetime.datetime.strptime(cptDate, "%d.%m.%Y %H:%M:%S")
    cptDate1 = cptDate1 - relativedelta(months = 1)
    cptDate1 = cptDate1.strftime("%d.%m.%Y %H:%M:%S")
    #print(cptDate, cptDate1)

    # get timestep number for crossplot date and previous date
    i = getTimeStepNumber(times, startDate, cptDate)
    j = getTimeStepNumber(times, startDate, cptDate1)


    if(i>=0 and j>=0):
        for x in wellNames:
            wi = (wellNames.index(x))
            # WQ filter !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if x[0:4] == "WQ2-" or x == "WQ-11" or x == "WQ-13":
                printCptByDate(ResArr, times, T, V, x, wi, cptDate, i, cptOutFile)
                printCptByDate(ResArr, times, T, V, x, wi, cptDate1, j, cptOutFile)
                cptOutFile.write('\n') # переход на новую строку
                #print()
    else:
        print("{0:s} - no such date".format(cptDate))


    cptOutFile.close()


#   # debug part
#   with open("../testDateList","r") as dateList:
#       for line in dateList:
#           i = getTimeStepNumber(times, startDate, line.strip('\n'))
#           if(i>=0):
#
#               for x in wellNames:
#                   wi = (wellNames.index(x))
#                   ##debug output
#                   #print('{0:s} - timestep={1:4d}  tos = {2:5.11f} '.format(line.strip('\n'), i, times[i].tos),end= ' ' ) 
#
#                   print('{0:s} {1:5.2f} '.format(line.strip('\n'), times[i].tos), end = ' ' ) 
#
#                   print('{0:s}'.format(x), end = ' ') # вывод имени скважины
#                   
#                   print('{0:3f}'.format(ResArr[T*V*wi + T*cts.Sopt + i]), end = ' ')  # вывод расчетной накопленной добычи нефти
#                   print('{0:3f}'.format(ResArr[T*V*wi + T*cts.Hopt + i]), end = ' ')  # вывод фактической накопленной добычи нефти
#
#                   print(' ',end=' ')
#
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Swit + i]), end = ' ')  # вывод расчетной накопленной закачки 
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Hwit + i]), end = ' ')  # вывод фактической накопленной закачки 
#
#                   print(' ',end=' ')
#
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Swpt + i]), end = ' ')  # вывод расчетной накопленной добычи воды 
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Hwpt + i]), end = ' ')  # вывод фактической накопленной добычи воды 
#                   
#                   print(' ',end=' ')
#
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Sbhp + i]), end = ' ')  # вывод расчетного забойного давления                
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Hbhp + i]), end = ' ')  # вывод фактического забойного давления                
#                   
#                   print()
#
#           else:
#               print("{0:s} - no such date".format(line.strip('\n')))


        

#    dateList.close()





