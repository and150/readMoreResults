import  datetime
#��������� ����(������) �� �������� (��� � ������� float)
def DatesCompare(sdate="31.12.2001 00:00:00", time=0.0, sdatArr=[]):
    SDAT = datetime.datetime.strptime(str(sdatArr[2])+"-"+str(sdatArr[1])+"-"+str(sdatArr[0]),"%Y-%m-%d")
    date = datetime.datetime.strptime(sdate,"%d.%m.%Y %H:%M:%S")
    time1 = date - SDAT
    time1= time1.days + time1.seconds/60/60/24
    return time - time1

def date2days(sdate="31.12.2001 00:00:00", sDate = []):
#������� ����� ���� � ������� ��.��.���� ��:��:�� ������������ �� � ��� � 
# �������� �� ��� ���� ������ �������� ����� ���������� � �������� ������ ��������� ����� �� RATE-�����    
    initDate = datetime.datetime.strptime(str(sDate[2])+"-"+str(sDate[1])+"-"+str(sDate[0]),"%Y-%m-%d")  # ����������� ��������� ���� �� ������� �� �����   
    date = datetime.datetime.strptime(sdate,"%d.%m.%Y %H:%M:%S")    # ����������� ���� �� ������� ��.��.���� ��:��:�� �� �����
    time = date - initDate    # ������ ��������� ������� �� ������ �������
    time =   time.days + time.seconds/60/60/24 # ������� ���������� ��������� � ���
    return time



