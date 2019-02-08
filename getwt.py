import constants as cts
import datetime
import time
from datescompare import *

#################### вспомогательные функции и классы для списка испытаний ###########################
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


    wtFileName   = currDir+"\\"+rootName+".WTlist"  # имя входного файла со списком исследований
    outFile  = open(currDir+"\\"+rootName+".WTgraphs", "w") # выходной файл графиков исследований
    wtOutFile = open(currDir+"\\"+rootName+".WTout","w") # выходной файл с параметрами КВД
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # заголовок таблицы параметров КВД        

    ####### обработка списка испытаний #######
    WTlist = GetWTlist(wtFileName, startDate)  #получает список испытаний скважин (нужно в программе научиться его сортировать по скважинам и по датам, но пока обязательно делать это перед загрузкой)
      

    #### поиск индекса скважины в массиве Item
    tr = 0
    timetol = cts.TIMETOL
    liqCut = cts.LIQCUT
    PBUstr = ""
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во ячеек по вертикали, нужно сюда передавать параметр
    V = cts.VEC + MZ*2*numsArray[55-1]       # количество векторов 


    for x in WTlist: # для всех скважино-испытаний в списке
        PBUstr = ""
        wi = (wellNames.index(x.well))     
        for i in range(0,T): # для всех временных записей RATE файла
            #вывод показателей только в интервале испытаний
            if(times[i].tos >= x.start and times[i].tos <= x.stop):             
            #if(x.start - times[i].tos < timetol and times[i].tos - x.stop < timetol):                
                #вывод всех показателей по испытаниям скважин в файл *.WTgraphs  без фильтрации 
                outFile.write("\n")
                outFile.write("WT=" + str(x.wt)+ " ")                            #вывод номера испытания
                outStr = str(times[i].tos) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # вывод времени и номера скважины                              

                outFile.write(str(ResArr[T*V*wi + T* cts.Sbhp + i])); outFile.write(" ")  # вывод расчетного забойного давления                
                outFile.write(str(ResArr[T*V*wi + T* cts.Sopr + i])); outFile.write(" ")  # вывод расчетного дебита нефти                
                outFile.write(str(ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i])); outFile.write(" ")  # вывод расчетного дебита воды + закачка

                outFile.write(str(ResArr[T*V*wi + T* cts.Hbhp + i])); outFile.write(" ")  # вывод фактического забойного давления                
                outFile.write(str(ResArr[T*V*wi + T* cts.Hopr + i])); outFile.write(" ")  # вывод фактического дебита нефти                
                outFile.write(str(ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i])); outFile.write(" ")  # вывод фактического дебита воды + закачка
                


                #поиск PBU и вытаскивание параметров для вывода в отдельную таблицу *.WTout
                # расчет дебитов жидкости в интервале PBU    
                currLiq  = ResArr[T*V*wi + T* cts.Sopr + i] + ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i]# текущий расчетный дебит жидкости
                currLiqH = ResArr[T*V*wi + T* cts.Hopr + i] + ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i]# текущий фактический дебит жидкости


                currP  = ResArr[T*V*wi + T* cts.Sbhp + i]   #расчетное давление 
                currPH = ResArr[T*V*wi + T* cts.Hbhp + i]   #фактическое давление 
                if currP <= cts.PTOL or currPH <= cts.PTOL :
                    maxP = maxP
                    maxPH = maxPH
                else:
                    maxP = currP
                    maxPH = currPH


                if i<=len(times):  nextLiq = ResArr[T*V*wi + T* cts.Sopr + i+1] + ResArr[T*V*wi + T* cts.Swpr + i+1]+ ResArr[T*V*wi + T* cts.Swir + i+1] # следующий расчетный дебит жидкости                   
                else: nextLiq = currLiq
    
                if(currLiq > liqCut):   # проверка интервалов с ненулевым дебитом 
                    outFile.write(" dynamic") 
                    if(nextLiq <= liqCut):                          
                        PBUstr = PBUstr + x.well + " " + str(times[i].tos) #имя скважины и время начала КВД
                        PBUstr = PBUstr + " " + str(currLiq) + " " + str(currLiqH) # расчетный и фактический дебит(приемистость) жидкости
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Sbhp + i]) #расчетное забойное 
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Hbhp + i])  #фактическое забойное
                else:
                    outFile.write(" static")                    
                    if(nextLiq > liqCut): 
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Sbhp + i])   #расчетное пластовое
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Hbhp + i])   #фактическое пластовое
                        #PBUstr = PBUstr + " " + str(maxP)   #расчетное пластовое
                        #PBUstr = PBUstr + " " + str(maxPH)   #фактическое пластовое
                        #PBUstr = PBUstr + " " + str(times[i].tos)  # время окончания КВД                       
                        break # прерывает цикл после прочтения ПЕРВОЙ КВД для скважины!
        #print(str(x.wt)," ", PBUstr) # вывод параметров PBU в консоль
        PBUstr = PBUstr + " " + str(maxP)   #расчетное пластовое
        PBUstr = PBUstr + " " + str(maxPH)   #фактическое пластовое
        PBUstr = PBUstr + " " + str(times[i].tos)  # время окончания КВД                       

        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n") #вывод параметров PBU в файл        
    outFile.close()
    wtOutFile.close()
    ###### окончание обработки испытаний ######
