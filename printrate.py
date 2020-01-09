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

                print(str(ResArr[T*V*wi+T*cts.i_d['Sbhp']+i]), end = ' ')  # simulated BHP
                print(str(ResArr[T*V*wi+T*cts.i_d['Hbhp']+i]), end = ' ')  # historic BHP
                print(str(ResArr[T*V*wi+T*cts.i_d['Sopr']+i]), end = ' ')  # simulated oil rate
                print(str(ResArr[T*V*wi+T*cts.i_d['Hopr']+i]), end = ' ')  # historic oil rate
                print(str(ResArr[T*V*wi+T*cts.i_d['Swir']+i]), end = ' ')  # simulated injection rate
                print(str(ResArr[T*V*wi+T*cts.i_d['Hwir']+i]), end = ' ')  # historic injection rate
                print(str(ResArr[T*V*wi+T*cts.i_d['Swpr']+i]), end = ' ')  # simulated water rate
                print(str(ResArr[T*V*wi+T*cts.i_d['Hwpr']+i]), end = ' ')  # historic water rate

                print(str(ResArr[T*V*wi+T*cts.i_d['Hwefa']+i]), end = ' ')  # wefac output

                print(str(ResArr[T*V*wi+T*cts.i_d['Sopt']+i]), end = ' ')  # simulated cumulative oil production
                print(str(ResArr[T*V*wi+T*cts.i_d['Hopt']+i]), end = ' ')  # historic cumulative oil production
                print(str(ResArr[T*V*wi+T*cts.i_d['Swit']+i]), end = ' ')  # simulated cumulative injection
                print(str(ResArr[T*V*wi+T*cts.i_d['Hwit']+i]), end = ' ')  # historic cumulative injection
                print(str(ResArr[T*V*wi+T*cts.i_d['Swpt']+i]), end = ' ')  # simulated cumulative water production
                print(str(ResArr[T*V*wi+T*cts.i_d['Hwpt']+i]), end = ' ')  # historic cumulative water production

                print()
