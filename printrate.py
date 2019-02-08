import constants as cts
from datescompare import *

def printRate(times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]


    MZ = numsArray[5-1] # ���������� ����� � ��������� (���-�� ����� �� ���������, ����� ���� ���������� ��������
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    V = cts.VEC + MZ*2*numsArray[55-1]       # ���������� �������� 

    for x in wellNames:
        wi = (wellNames.index(x))
        for i in range(0,T):
                print(str(times[i]) +" " + str(wellNames[wi]+" "),end = ' ') # ����� ������� � ������ ��������                              

                print(str(ResArr[T*V*wi + T*cts.Sbhp + i]), end = ' ')  # ����� ���������� ��������� ��������                
                print(str(ResArr[T*V*wi + T*cts.Sopr + i]), end = ' ')  # ����� ���������� ������ �����                
                print(str(ResArr[T*V*wi + T*cts.Swpr + i]), end = ' ')  # ����� ���������� ������ ����                
                print(str(ResArr[T*V*wi + T*cts.Swir + i]), end = ' ')  # ����� ��������� ������������ 

                print(str(ResArr[T*V*wi + T*cts.Hbhp + i]), end = ' ')  # ����� ������������ ��������� ��������                
                print(str(ResArr[T*V*wi + T*cts.Hopr + i]), end = ' ')  # ����� ������������ ������ �����                
                print(str(ResArr[T*V*wi + T*cts.Hwpr + i]), end = ' ')  # ����� ������������ ������ ����
                print(str(ResArr[T*V*wi + T*cts.Hwir + i]), end = ' ')  # ����� ����������� ������������ 

                print(str(ResArr[T*V*wi + T*cts.Hwefa + i]), end = ' ')  # ����� ������������ ������������ 

                print(str(ResArr[T*V*wi + T*cts.Sopt + i]), end = ' ')  # ����� ��������� ����������� ������ �����
                print(str(ResArr[T*V*wi + T*cts.Swpt + i]), end = ' ')  # ����� ��������� ����������� ������ ���� 
                print(str(ResArr[T*V*wi + T*cts.Swit + i]), end = ' ')  # ����� ��������� ����������� ������� 
                print()
 
