#-*- coding:utf-8 -*-
import constants as cts
from datescompare import *

def printRate(times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]


    MZ = numsArray[5-1] # number of layers in wells 
    T = len(times) # amount of rate entries 
    W = len(wellNames) # wells amount
    V = cts.VEC + MZ*2*numsArray[55-1]       # vectors amount

    for x in wellNames:
        wi = (wellNames.index(x))
        for i in range(0,T):
                print(str(times[i].tos) +" " + str(wellNames[wi]+" "),end = ' ') # time and well name output

                print(str(ResArr[T*V*wi + T*cts.Sbhp + i]), end = ' ')  # simulated BHP
                print(str(ResArr[T*V*wi + T*cts.Hbhp + i]), end = ' ')  # historic BHP
                print(str(ResArr[T*V*wi + T*cts.Sopr + i]), end = ' ')  # simulated oil rate
                print(str(ResArr[T*V*wi + T*cts.Hopr + i]), end = ' ')  # historic oil rate
                print(str(ResArr[T*V*wi + T*cts.Swir + i]), end = ' ')  # simulated injection rate
                print(str(ResArr[T*V*wi + T*cts.Hwir + i]), end = ' ')  # historic injection rate
                print(str(ResArr[T*V*wi + T*cts.Swpr + i]), end = ' ')  # simulated water rate
                print(str(ResArr[T*V*wi + T*cts.Hwpr + i]), end = ' ')  # historic water rate

                print(str(ResArr[T*V*wi + T*cts.Hwefa + i]), end = ' ')  # wefac output

                print(str(ResArr[T*V*wi + T*cts.Sopt + i]), end = ' ')  # simulated cumulative oil production
                print(str(ResArr[T*V*wi + T*cts.Hopt + i]), end = ' ')  # historic cumulative oil production
                print(str(ResArr[T*V*wi + T*cts.Swit + i]), end = ' ')  # simulated cumulative injection
                print(str(ResArr[T*V*wi + T*cts.Hwit + i]), end = ' ')  # historic cumulative injection
                print(str(ResArr[T*V*wi + T*cts.Swpt + i]), end = ' ')  # simulated cumulative water production
                print(str(ResArr[T*V*wi + T*cts.Hwpt + i]), end = ' ')  # historic cumulative water production

                print()
 
