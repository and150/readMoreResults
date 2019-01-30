import struct
import constants
import datetime
import time
from datescompare import *


def getBinData(bts, type="int",size=1,pr=0):
#read binary data from file stream and return array of tuples
    ARRAY = [0]*size
    if (type=='int'):
       for i in range(0,size):
            ARRAY[i] =  struct.unpack('i',bts.read(4))[0]
    elif (type=='float'):
        for i in range(0,size):
            ARRAY[i] = struct.unpack('f',bts.read(4))[0]
    elif (type=='char'):
        for i in range(0,size):
            ARRAY[i]=  str(struct.unpack('c',bts.read(1))[0], 'utf-8')  #read 1 char
    elif (type=='char4'):
        for i in range(0,size):
            ARRAY[i]=  str(b''.join(struct.unpack('c'*4,bts.read(4))), 'utf-8')  #read word of 4 chars
    elif (type=='char16'):
        for i in range(0,size):
            ARRAY[i]= str(b''.join(struct.unpack('c'*16,bts.read(16))), 'utf-8') #read word of 16 chars
    else: return 0
    if(pr==1): print (ARRAY) #comment to stop printing array
    return (ARRAY)




#сравнение даты(строка) со временем (дни в формате float)
def DatesCompare(sdate="31.12.2001 00:00:00", time=0.0, sdatArr=[]):
    SDAT = datetime.datetime.strptime(str(sdatArr[2])+"-"+str(sdatArr[1])+"-"+str(sdatArr[0]),"%Y-%m-%d")
    date = datetime.datetime.strptime(sdate,"%d.%m.%Y %H:%M:%S")
    time1 = date - SDAT
    time1= time1.days + time1.seconds/60/60/24
    return time - time1

def date2days(sdate="31.12.2001 00:00:00", sDate = []):
#функция берет дату в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС конвертирует ее в дни и 
# вычитает из нее дату начала расчетов чтобы сравнивать с массивом времен временных шагов из RATE-файла    
    initDate = datetime.datetime.strptime(str(sDate[2])+"-"+str(sDate[1])+"-"+str(sDate[0]),"%Y-%m-%d")  # конвертация стартовой даты из массива во время   
    date = datetime.datetime.strptime(sdate,"%d.%m.%Y %H:%M:%S")    # конвертация даты из формата ДД.ММ.ГГГГ ЧЧ:ММ:СС во время
    time = date - initDate    # расчет интервала времени от начала расчета
    time =   time.days + time.seconds/60/60/24 # перевод временного интервала в дни
    return time





#################### вспомогательные функции для вывода профилей притока и КВД #######################
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


def GetWTlist(filename, SDAT): 
    WTLIST = []
    lines = [line.rstrip('\n') for line in open (filename)] 
    for x in lines:
        if len(x)>0: 
            words = x.split()
            WTLIST.append(    WTItem( words[0]  ,  date2days(words[1]+" "+words[2], SDAT), date2days(words[3]+" "+words[4], SDAT) , words[5]  )                 )
            #print (words[1]+" "+words[2]," | ", words[3]+" "+words[4])
    return WTLIST




# функция чтения профилей притока (внутри константы для Мифрифа!!!!)
def getPLT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()



    pltFileName = currDir+"\\"+rootName+".PLTlist"  # имя входного файла со списком исследований PLT
    pltOutFile = open(currDir+"\\"+rootName+".PLTout","w") # файл вывода таблицы исследований PLT

    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во ячеек по вертикали, нужно сюда передавать параметр
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    V = constants.VEC + MZ*2       # количество векторов 

    # чтение списка PLT
    PLTlist = []       
    PLTlist = GetPLTlist(pltFileName,startDate)

    for x in PLTlist: # для всех скважино-профилеметрий в списке
        j = (wellNames.index(x.well))     
        # вывод прочитанных векторов в консоль для проверки    
        #for j in range(0,len(wellNames)):        
        for i in range(0,len(times)):
            if(times[i]== x.start): 
                #print(times[i], wellNames[j], end=" ")      #вывод времени и имени скважины
                #print(ResArr[T*V*j + T*2 + i], end=" ")     # вывод расчетного забойного давления
                #print(ResArr[T*V*j + T*0 + i], end=" ")     # вывод расчетного дебита нефти
                #print(ResArr[T*V*j + T*1 + i], end=" ")     # вывод расчетного дебита воды
                #print(ResArr[T*V*j + T*5 + i], end=" ")     # вывод расчетного забойного давления
                #print(ResArr[T*V*j + T*3 + i], end=" ")     # вывод расчетного дебита нефти
                #print(ResArr[T*V*j + T*4 + i], end=" | ")   # вывод расчетного дебита воды
    
#               # вывод расчетных дебитов по соединениям
#               for k in range(0,MZ):
#                   print(ResArr[T*V*j + T*(6+k) + i], end=" ")     # нефть
#               for k in range(0,MZ):
#                   print(ResArr[T*V*j + T*(6+MZ+k) + i], end=" ")     # вода
        
                pltarr = [0]*MZ 
                for k in range(0,MZ):
                    #print("{:.3f}".format(ResArr[T*V*j + T*(6+k) + i] + ResArr[T*V*j + T*(6+MZ+k) + i]), end=" ")     # жидкость  6 - количество скважинных векторов, MZ- количество соединений
                    pltarr[k] = ResArr[T*V*j + T*(6+k) + i] + ResArr[T*V*j + T*(6+MZ+k) + i] # генерация временного вектора PLT на каждый временной шаг для каждой скважины
                #вывод на консоль
                #print(pltarr)
                #print(sum(pltarr[0:4]), sum(pltarr[4:7]) ,sum(pltarr[7:10]), end = " ") # вывод суммы по пачкам (индексы надо ВРУЧНУЮ проставить...)
                #print(sum(pltarr[0:34]), sum(pltarr[34:56]), sum(pltarr[56:66]), sum(pltarr[66:75]), sum(pltarr[75:89]), end = " ") # вывод суммы по пачкам (индексы надо ВРУЧНУЮ проставить...)
                #print()  

                #вывод в файл 
                pltLR = sum(pltarr) 
                if pltLR != 0: 
                #    pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f}\n'.format(times[i], wellNames[j], sum(pltarr[0:4])/pltLR, sum(pltarr[4:7])/pltLR, sum(pltarr[7:10])/pltLR) )                    
                   if wellNames[j] == 'WQ2-197':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} - - - \n'.format( times[i], wellNames[j],  sum(pltarr[0:46])/pltLR, sum(pltarr[46:65])/pltLR )  )                  
                   elif  wellNames[j]== 'WQ2-246':
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} - - \n'.format( times[i], wellNames[j],  sum(pltarr[0:40])/pltLR, sum(pltarr[40:68])/pltLR, sum(pltarr[68:89])/pltLR )  )                  
                   else:                	
                       pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}\n'.format( times[i], wellNames[j],  sum(pltarr[0:34])/pltLR, sum(pltarr[34:56])/pltLR, sum(pltarr[56:66])/pltLR, sum(pltarr[66:75])/pltLR, sum(pltarr[75:89])/pltLR  ) )                    
                else:
                	pltOutFile.write( '{} {} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} liquid rate == 0\n'.format( times[i], wellNames[j],  0, 0, 0, 0, 0  ) )                                    
    ###### окончание обработки испытаний ######




def getWT(currDir, rootName, startDate, times, numsArray, RateOut):

    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()


    wtFileName   = currDir+"\\"+rootName+".WTlist"  # имя входного файла со списком исследований
    outFile  = open(currDir+"\\"+rootName+".results", "w") # выходной файл графиков исследований
    wtOutFile = open(currDir+"\\"+rootName+".WTout","w") # выходной файл с параметрами КВД
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # заголовок таблицы параметров КВД        

    ####### обработка списка испытаний #######
    WTlist = GetWTlist(wtFileName, startDate)  #получает список испытаний скважин (нужно в программе научиться его сортировать по скважинам и по датам, но пока обязательно делать это перед загрузкой)
      

    #### поиск индекса скважины в массиве Item
    tr = 0
    timetol = 0.001
    liqCut = 0.0155
    PBUstr = ""
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    V = constants.VEC            # количество векторов 

    for x in WTlist: # для всех скважино-испытаний в списке
        PBUstr = ""
        wi = (wellNames.index(x.well))     
        for i in range(0,T): # для всех временных записей RATE файла
            #вывод показателей только в интервале испытаний
            if(times[i]>= x.start and times[i]<= x.stop):             
            #if(x.start - times[i] < timetol and times[i] - x.stop < timetol):                
                #вывод всех показателей по испытаниям скважин в файл *.results  без фильтрации 
                outFile.write("\n")
                outFile.write("WT=" + str(x.wt)+ " ")                            #вывод номера испытания
                outStr = str(times[i]) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # вывод времени и номера скважины                              
                outFile.write(str(ResArr[T*V*wi + T*2 + i])); outFile.write(" ")  # вывод расчетного забойного давления                
                outFile.write(str(ResArr[T*V*wi + T*0 + i])); outFile.write(" ")  # вывод расчетного дебита нефти                
                outFile.write(str(ResArr[T*V*wi + T*1 + i])); outFile.write(" ")  # вывод расчетного дебита воды                
                outFile.write(str(ResArr[T*V*wi + T*5 + i])); outFile.write(" ")  # вывод фактического забойного давления                
                outFile.write(str(ResArr[T*V*wi + T*3 + i])); outFile.write(" ")  # вывод фактического дебита нефти                
                outFile.write(str(ResArr[T*V*wi + T*4 + i])); outFile.write(" ")  # вывод фактического дебита воды
                

                #поиск PBU и вытаскивание параметров для вывода в отдельную таблицу *.WTout
                # расчет дебитов жидкости в интервале PBU    
                currLiq  = ResArr[T*V*wi + T*0 + i] + ResArr[T*V*wi + T*1 + i] # текущий расчетный дебит жидкости
                currLiqH = ResArr[T*V*wi + T*3 + i] + ResArr[T*V*wi + T*4 + i] # текущий фактический дебит жидкости
                if i<=len(times):  nextLiq = ResArr[T*V*wi + T*0 + i+1] + ResArr[T*V*wi + T*1 + i+1] # следующий расчетный дебит жидкости                   
                else: nextLiq = currLiq
    
                if(currLiq > liqCut):   # проверка интервалов с ненулевым дебитом 
                    outFile.write(" dynamic") 
                    if(nextLiq <= liqCut):                          
                        PBUstr = PBUstr + x.well + " " + str(times[i]) #имя скважины и время начала КВД
                        PBUstr = PBUstr + " " + str(currLiq) + " " + str(currLiqH) # расчетный и фактический дебит(приемистость) жидкости
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*2 + i]) #расчетное забойное 
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*5 + i])  #фактическое забойное
                else:
                    outFile.write(" static")                    
                    if(nextLiq > liqCut): 
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*2 + i])   #расчетное пластовое
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*5 + i])   #фактическое пластовое
                        PBUstr = PBUstr + " " + str(times[i])  # время окончания КВД                       
                        break # прерывает цикл после прочтения ПЕРВОЙ КВД для скважины!
        #print(str(x.wt)," ", PBUstr) # вывод параметров PBU в консоль
        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n") #вывод параметров PBU в файл        
    outFile.close()
    wtOutFile.close()
    ###### окончание обработки испытаний ######

