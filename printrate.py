import constants as cts
from datescompare import *

def printRate(times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]


    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во ячеек по вертикали, нужно сюда передавать параметр
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    V = cts.VEC + MZ*2*numsArray[55-1]       # количество векторов 

    for x in wellNames:
        wi = (wellNames.index(x))
        for i in range(0,T):
                print(str(times[i]) +" " + str(wellNames[wi]+" "),end = ' ') # вывод времени и номера скважины                              
                print(str(ResArr[T*V*wi + T*cts.Sbhp + i]), end = ' ')  # вывод расчетного забойного давления                
                print(str(ResArr[T*V*wi + T*cts.Sopr + i]), end = ' ')  # вывод расчетного дебита нефти                
                print(str(ResArr[T*V*wi + T*cts.Swpr + i]), end = ' ')  # вывод расчетного дебита воды                
                print(str(ResArr[T*V*wi + T*cts.Hbhp + i]), end = ' ')  # вывод фактического забойного давления                
                print(str(ResArr[T*V*wi + T*cts.Hopr + i]), end = ' ')  # вывод фактического дебита нефти                
                print(str(ResArr[T*V*wi + T*cts.Hwpr + i]), end = ' ')  # вывод фактического дебита воды

                print(str(ResArr[T*V*wi + T*cts.Hwefa + i]), end = ' ')  # вывод коэффициента эксплуатации 

                print(str(ResArr[T*V*wi + T*cts.Sopt + i]), end = ' ')  # вывод расчетной накопленной добычи нефти
                print(str(ResArr[T*V*wi + T*cts.Swpt + i]), end = ' ')  # вывод расчетной накопленной добычи воды 
                print(str(ResArr[T*V*wi + T*cts.Swit + i]), end = ' ')  # вывод расчетной накопленной закачки 
                print()
 
