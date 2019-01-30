import constants
from datescompare import *

def printRate(times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]


    MZ = numsArray[5-1] # ���������� ����� � ��������� (���-�� ����� �� ���������, ����� ���� ���������� ��������
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    V = constants.VEC + MZ*2*numsArray[55-1]       # ���������� �������� 

    for x in wellNames:
        wi = (wellNames.index(x))
        for i in range(0,T):
                print(str(times[i]) +" " + str(wellNames[wi]+" "),end = ' ') # ����� ������� � ������ ��������                              
                print(str(ResArr[T*V*wi + T*2 + i]), end = ' ')  # ����� ���������� ��������� ��������                
                print(str(ResArr[T*V*wi + T*0 + i]), end = ' ')  # ����� ���������� ������ �����                
                print(str(ResArr[T*V*wi + T*1 + i]), end = ' ')  # ����� ���������� ������ ����                
                print(str(ResArr[T*V*wi + T*5 + i]), end = ' ')  # ����� ������������ ��������� ��������                
                print(str(ResArr[T*V*wi + T*3 + i]), end = ' ')  # ����� ������������ ������ �����                
                print(str(ResArr[T*V*wi + T*4 + i]), end = '\n')  # ����� ������������ ������ ����
 
