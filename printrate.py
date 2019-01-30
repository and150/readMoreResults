import constants
from datescompare import *

def printRate(times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]


    MZ = numsArray[5-1] # количество слоев в скважинах (кол-во ячеек по вертикали, нужно сюда передавать параметр
    T = len(times) # количество записей RATE
    W = len(wellNames) # количество скважин
    V = constants.VEC + MZ*2*numsArray[55-1]       # количество векторов 

    for x in wellNames:
        wi = (wellNames.index(x))
        for i in range(0,T):
                print(str(times[i]) +" " + str(wellNames[wi]+" "),end = ' ') # вывод времени и номера скважины                              
                print(str(ResArr[T*V*wi + T*2 + i]), end = ' ')  # вывод расчетного забойного давления                
                print(str(ResArr[T*V*wi + T*0 + i]), end = ' ')  # вывод расчетного дебита нефти                
                print(str(ResArr[T*V*wi + T*1 + i]), end = ' ')  # вывод расчетного дебита воды                
                print(str(ResArr[T*V*wi + T*5 + i]), end = ' ')  # вывод фактического забойного давления                
                print(str(ResArr[T*V*wi + T*3 + i]), end = ' ')  # вывод фактического дебита нефти                
                print(str(ResArr[T*V*wi + T*4 + i]), end = '\n')  # вывод фактического дебита воды
 
