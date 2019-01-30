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





#################### ��������������� ������� ��� ������ �������� ������� � ��� #######################
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




# ������� ������ �������� ������� (������ ��������� ��� �������!!!!)
def getPLT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()



    pltFileName = currDir+"\\"+rootName+".PLTlist"  # ��� �������� ����� �� ������� ������������ PLT
    pltOutFile = open(currDir+"\\"+rootName+".PLTout","w") # ���� ������ ������� ������������ PLT

    MZ = numsArray[5-1] # ���������� ����� � ��������� (���-�� ����� �� ���������, ����� ���� ���������� ��������
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    V = constants.VEC + MZ*2       # ���������� �������� 

    # ������ ������ PLT
    PLTlist = []       
    PLTlist = GetPLTlist(pltFileName,startDate)

    for x in PLTlist: # ��� ���� ��������-������������� � ������
        j = (wellNames.index(x.well))     
        # ����� ����������� �������� � ������� ��� ��������    
        #for j in range(0,len(wellNames)):        
        for i in range(0,len(times)):
            if(times[i]== x.start): 
                #print(times[i], wellNames[j], end=" ")      #����� ������� � ����� ��������
                #print(ResArr[T*V*j + T*2 + i], end=" ")     # ����� ���������� ��������� ��������
                #print(ResArr[T*V*j + T*0 + i], end=" ")     # ����� ���������� ������ �����
                #print(ResArr[T*V*j + T*1 + i], end=" ")     # ����� ���������� ������ ����
                #print(ResArr[T*V*j + T*5 + i], end=" ")     # ����� ���������� ��������� ��������
                #print(ResArr[T*V*j + T*3 + i], end=" ")     # ����� ���������� ������ �����
                #print(ResArr[T*V*j + T*4 + i], end=" | ")   # ����� ���������� ������ ����
    
#               # ����� ��������� ������� �� �����������
#               for k in range(0,MZ):
#                   print(ResArr[T*V*j + T*(6+k) + i], end=" ")     # �����
#               for k in range(0,MZ):
#                   print(ResArr[T*V*j + T*(6+MZ+k) + i], end=" ")     # ����
        
                pltarr = [0]*MZ 
                for k in range(0,MZ):
                    #print("{:.3f}".format(ResArr[T*V*j + T*(6+k) + i] + ResArr[T*V*j + T*(6+MZ+k) + i]), end=" ")     # ��������  6 - ���������� ���������� ��������, MZ- ���������� ����������
                    pltarr[k] = ResArr[T*V*j + T*(6+k) + i] + ResArr[T*V*j + T*(6+MZ+k) + i] # ��������� ���������� ������� PLT �� ������ ��������� ��� ��� ������ ��������
                #����� �� �������
                #print(pltarr)
                #print(sum(pltarr[0:4]), sum(pltarr[4:7]) ,sum(pltarr[7:10]), end = " ") # ����� ����� �� ������ (������� ���� ������� ����������...)
                #print(sum(pltarr[0:34]), sum(pltarr[34:56]), sum(pltarr[56:66]), sum(pltarr[66:75]), sum(pltarr[75:89]), end = " ") # ����� ����� �� ������ (������� ���� ������� ����������...)
                #print()  

                #����� � ���� 
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
    ###### ��������� ��������� ��������� ######




def getWT(currDir, rootName, startDate, times, numsArray, RateOut):

    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()


    wtFileName   = currDir+"\\"+rootName+".WTlist"  # ��� �������� ����� �� ������� ������������
    outFile  = open(currDir+"\\"+rootName+".results", "w") # �������� ���� �������� ������������
    wtOutFile = open(currDir+"\\"+rootName+".WTout","w") # �������� ���� � ����������� ���
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # ��������� ������� ���������� ���        

    ####### ��������� ������ ��������� #######
    WTlist = GetWTlist(wtFileName, startDate)  #�������� ������ ��������� ������� (����� � ��������� ��������� ��� ����������� �� ��������� � �� �����, �� ���� ����������� ������ ��� ����� ���������)
      

    #### ����� ������� �������� � ������� Item
    tr = 0
    timetol = 0.001
    liqCut = 0.0155
    PBUstr = ""
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    V = constants.VEC            # ���������� �������� 

    for x in WTlist: # ��� ���� ��������-��������� � ������
        PBUstr = ""
        wi = (wellNames.index(x.well))     
        for i in range(0,T): # ��� ���� ��������� ������� RATE �����
            #����� ����������� ������ � ��������� ���������
            if(times[i]>= x.start and times[i]<= x.stop):             
            #if(x.start - times[i] < timetol and times[i] - x.stop < timetol):                
                #����� ���� ����������� �� ���������� ������� � ���� *.results  ��� ���������� 
                outFile.write("\n")
                outFile.write("WT=" + str(x.wt)+ " ")                            #����� ������ ���������
                outStr = str(times[i]) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # ����� ������� � ������ ��������                              
                outFile.write(str(ResArr[T*V*wi + T*2 + i])); outFile.write(" ")  # ����� ���������� ��������� ��������                
                outFile.write(str(ResArr[T*V*wi + T*0 + i])); outFile.write(" ")  # ����� ���������� ������ �����                
                outFile.write(str(ResArr[T*V*wi + T*1 + i])); outFile.write(" ")  # ����� ���������� ������ ����                
                outFile.write(str(ResArr[T*V*wi + T*5 + i])); outFile.write(" ")  # ����� ������������ ��������� ��������                
                outFile.write(str(ResArr[T*V*wi + T*3 + i])); outFile.write(" ")  # ����� ������������ ������ �����                
                outFile.write(str(ResArr[T*V*wi + T*4 + i])); outFile.write(" ")  # ����� ������������ ������ ����
                

                #����� PBU � ������������ ���������� ��� ������ � ��������� ������� *.WTout
                # ������ ������� �������� � ��������� PBU    
                currLiq  = ResArr[T*V*wi + T*0 + i] + ResArr[T*V*wi + T*1 + i] # ������� ��������� ����� ��������
                currLiqH = ResArr[T*V*wi + T*3 + i] + ResArr[T*V*wi + T*4 + i] # ������� ����������� ����� ��������
                if i<=len(times):  nextLiq = ResArr[T*V*wi + T*0 + i+1] + ResArr[T*V*wi + T*1 + i+1] # ��������� ��������� ����� ��������                   
                else: nextLiq = currLiq
    
                if(currLiq > liqCut):   # �������� ���������� � ��������� ������� 
                    outFile.write(" dynamic") 
                    if(nextLiq <= liqCut):                          
                        PBUstr = PBUstr + x.well + " " + str(times[i]) #��� �������� � ����� ������ ���
                        PBUstr = PBUstr + " " + str(currLiq) + " " + str(currLiqH) # ��������� � ����������� �����(������������) ��������
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*2 + i]) #��������� �������� 
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*5 + i])  #����������� ��������
                else:
                    outFile.write(" static")                    
                    if(nextLiq > liqCut): 
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*2 + i])   #��������� ���������
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*5 + i])   #����������� ���������
                        PBUstr = PBUstr + " " + str(times[i])  # ����� ��������� ���                       
                        break # ��������� ���� ����� ��������� ������ ��� ��� ��������!
        #print(str(x.wt)," ", PBUstr) # ����� ���������� PBU � �������
        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n") #����� ���������� PBU � ����        
    outFile.close()
    wtOutFile.close()
    ###### ��������� ��������� ��������� ######

