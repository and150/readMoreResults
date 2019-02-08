import constants as cts
import datetime
import time
from datescompare import *

#################### вспомогательные функции дл€ вывода профилей притока #######################
class WTItem:
    def __init__(self, well="", start = 0.0, stop = 0.0, wt = 0):    
        self.well = well     # well name
        self.wt = wt         # wt number
        self.start = start   # well test start
        self.stop = stop    # well test end  
    def printList(self):
        print(self.well, self.start, self.stop, self.wt)  


def GetPLTlist(filename, SDAT):
    PLTLIST = []
    lines = [line.rstrip('\n') for line in open (filename)] 
    for x in lines:
        if len(x)>0: 
            words = x.split()
            PLTLIST.append( WTItem( words[0], date2days(words[1]+" "+words[2], SDAT))   )
    return PLTLIST






def getPLT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()



    pltFileName = currDir+"\\"+rootName+".PLTlist"  # им€ входного файла со списком исследований PLT
    pltOutFile = open(currDir+"\\"+rootName+".PLTout","w") # файл вывода таблицы исследований PLT

    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во €чеек по вертикали, нужно сюда передавать параметр
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    V = cts.VEC + MZ*2*numsArray[55-1]       # vectors amount 

    # чтение списка PLT
    PLTlist = []       
    PLTlist = GetPLTlist(pltFileName,startDate)

    for x in PLTlist: # дл€ всех скважино-профилеметрий в списке
        j = (wellNames.index(x.well))     
        # вывод прочитанных векторов в консоль дл€ проверки    
        #for j in range(0,len(wellNames)):        
        for i in range(0,len(times)):
            if(times[i].tos == x.start): 
                pltarr = [0]*MZ 
                for k in range(0,MZ):
                    #print("{:.3f}".format(ResArr[T*V*j + T*(6+k) + i] + ResArr[T*V*j + T*(6+MZ+k) + i]), end=" ")    # debug out
                    # генераци€ временного вектора PLT на каждый временной шаг дл€ каждой скважины
                    # жидкость  V - количество основных скважинных векторов, MZ- количество соединений
                    pltarr[k] = ResArr[T*V*j + T*(V+k) + i] + ResArr[T*V*j + T*(V+MZ+k) + i] 
                #вывод на консоль
                #print(pltarr)
                #print(sum(pltarr[0:4]), sum(pltarr[4:7]) ,sum(pltarr[7:10]), end = " ") # вывод суммы по пачкам (индексы надо ¬–”„Ќ”ё проставить...)
                #print(sum(pltarr[0:34]), sum(pltarr[34:56]), sum(pltarr[56:66]), sum(pltarr[66:75]), sum(pltarr[75:89]), end = " ") # вывод суммы по пачкам (индексы надо ¬–”„Ќ”ё проставить...)
                #print()  

                #вывод в файл 
                pltLR = sum(pltarr) 
                if pltLR != 0: 
                #    pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f}\n'.format(times[i].tos, wellNames[j], sum(pltarr[0:4])/pltLR, sum(pltarr[4:7])/pltLR, sum(pltarr[7:10])/pltLR) )                    
                   if wellNames[j] == 'WQ2-197':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} - - - \n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:46])/pltLR, sum(pltarr[46:89])/pltLR )  )                  
                   elif  wellNames[j]== 'WQ2-246':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} - - \n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:40])/pltLR, sum(pltarr[40:68])/pltLR, sum(pltarr[68:89])/pltLR )  )                  
                   elif  wellNames[j]== 'WQ2-75':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} - - \n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:40])/pltLR, sum(pltarr[40:66])/pltLR, sum(pltarr[66:89])/pltLR )  )                  
                   elif  wellNames[j]== 'WQ2-267':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} - - \n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:44])/pltLR, sum(pltarr[45:53])/pltLR, sum(pltarr[54:89])/pltLR )  )                  
                   elif  wellNames[j]== 'WQ2-189':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} {:.3f} - \n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:39])/pltLR, sum(pltarr[39:54])/pltLR, sum(pltarr[54:75])/pltLR , sum(pltarr[75:89])/pltLR)  )                  
                   elif  wellNames[j]== 'WQ2-20':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} {:.3f} - \n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:32])/pltLR, sum(pltarr[32:61])/pltLR, sum(pltarr[61:73])/pltLR , sum(pltarr[73:89])/pltLR)  )                  
                   else:                	
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}\n'.format( times[i].tos, wellNames[j],  sum(pltarr[0:34])/pltLR, sum(pltarr[34:56])/pltLR, sum(pltarr[56:66])/pltLR, sum(pltarr[66:75])/pltLR, sum(pltarr[75:89])/pltLR  ) )                    
                else:
                	pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} liquid rate == 0\n'.format( times[i].tos, wellNames[j],  0, 0, 0, 0, 0  ) )                                    
    ###### окончание обработки испытаний ######

