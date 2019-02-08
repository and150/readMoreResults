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

    cptOutFile = open(currDir+"\\"+rootName+".CPTout","w") # ���� ������ ����������� 
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    MZ = numsArray[5-1] # ���������� ����� � ��������� (���-�� ����� �� ���������, ����� ���� ���������� ��������
    V = cts.VEC + MZ*2*numsArray[55-1]       # ���������� �������� 

    #t0 = date2days("01.10.2018 00:00:00", startDate)
    #t1 = date2days("01.11.2018 00:00:00", startDate)
    printRate(times, numsArray, RateOut)




