import constants as cts
import datetime
import time
from datescompare import *

#################### ��������������� ������� � ������ ��� ������ ��������� ###########################
class WTItem:
    def __init__(self, well="", start = 0.0, stop = 0.0, wt = 0):    
        self.well = well     # well name
        self.wt = wt         # wt number
        self.start = start   # well test start
        self.stop = stop    # well test end  
    def printList(self):
        print(self.well, self.start, self.stop, self.wt)  


def GetWTlist(filename, SDAT): 
    WTLIST = []
    lines = [line.rstrip('\n') for line in open (filename)] 
    for x in lines:
        if len(x)>0: 
            words = x.split()
            WTLIST.append(    WTItem( words[0]  ,  date2days(words[1]+" "+words[2], SDAT), date2days(words[3]+" "+words[4], SDAT) , words[5]  )                 )
            #print (words[1]+" "+words[2]," | ", words[3]+" "+words[4])
    return WTLIST
 

def getWT(currDir, rootName, startDate, times, numsArray, RateOut):

    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()


    wtFileName   = currDir+"\\"+rootName+".WTlist"  # ��� �������� ����� �� ������� ������������
    outFile  = open(currDir+"\\"+rootName+".WTgraphs", "w") # �������� ���� �������� ������������
    wtOutFile = open(currDir+"\\"+rootName+".WTout","w") # �������� ���� � ����������� ���
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # ��������� ������� ���������� ���        

    ####### ��������� ������ ��������� #######
    WTlist = GetWTlist(wtFileName, startDate)  #�������� ������ ��������� ������� (����� � ��������� ��������� ��� ����������� �� ��������� � �� �����, �� ���� ����������� ������ ��� ����� ���������)
      

    #### ����� ������� �������� � ������� Item
    tr = 0
    timetol = cts.TIMETOL
    liqCut = cts.LIQCUT
    PBUstr = ""
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    MZ = numsArray[5-1] # ���������� ����� � ��������� (���-�� ����� �� ���������, ����� ���� ���������� ��������
    V = cts.VEC + MZ*2*numsArray[55-1]       # ���������� �������� 


    for x in WTlist: # ��� ���� ��������-��������� � ������
        PBUstr = ""
        wi = (wellNames.index(x.well))     
        for i in range(0,T): # ��� ���� ��������� ������� RATE �����
            #����� ����������� ������ � ��������� ���������
            if(times[i].tos >= x.start and times[i].tos <= x.stop):             
            #if(x.start - times[i].tos < timetol and times[i].tos - x.stop < timetol):                
                #����� ���� ����������� �� ���������� ������� � ���� *.WTgraphs  ��� ���������� 
                outFile.write("\n")
                outFile.write("WT=" + str(x.wt)+ " ")                            #����� ������ ���������
                outStr = str(times[i].tos) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # ����� ������� � ������ ��������                              

                outFile.write(str(ResArr[T*V*wi + T* cts.Sbhp + i])); outFile.write(" ")  # ����� ���������� ��������� ��������                
                outFile.write(str(ResArr[T*V*wi + T* cts.Sopr + i])); outFile.write(" ")  # ����� ���������� ������ �����                
                outFile.write(str(ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i])); outFile.write(" ")  # ����� ���������� ������ ���� + �������

                outFile.write(str(ResArr[T*V*wi + T* cts.Hbhp + i])); outFile.write(" ")  # ����� ������������ ��������� ��������                
                outFile.write(str(ResArr[T*V*wi + T* cts.Hopr + i])); outFile.write(" ")  # ����� ������������ ������ �����                
                outFile.write(str(ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i])); outFile.write(" ")  # ����� ������������ ������ ���� + �������
                


                #����� PBU � ������������ ���������� ��� ������ � ��������� ������� *.WTout
                # ������ ������� �������� � ��������� PBU    
                currLiq  = ResArr[T*V*wi + T* cts.Sopr + i] + ResArr[T*V*wi + T* cts.Swpr + i] + ResArr[T*V*wi + T* cts.Swir + i]# ������� ��������� ����� ��������
                currLiqH = ResArr[T*V*wi + T* cts.Hopr + i] + ResArr[T*V*wi + T* cts.Hwpr + i] + ResArr[T*V*wi + T* cts.Hwir + i]# ������� ����������� ����� ��������

                #currOil  = ResArr[T*V*wi + T* cts.Sopr + i] # ������� ��������� ����� �����
                #currOilH = ResArr[T*V*wi + T* cts.Hopr + i] # ������� ����������� ����� �����

                currP  = ResArr[T*V*wi + T* cts.Sbhp + i]   #��������� �������� 
                currPH = ResArr[T*V*wi + T* cts.Hbhp + i]   #����������� �������� 
                maxP = currP
                maxPH = currPH
                if currP <= cts.PTOL or currPH <= cts.PTOL :
                    maxP = maxP
                    maxPH = maxPH
                else:
                    maxP = currP
                    maxPH = currPH


                if i<=len(times):  nextLiq = ResArr[T*V*wi + T* cts.Sopr + i+1] + ResArr[T*V*wi + T* cts.Swpr + i+1]+ ResArr[T*V*wi + T* cts.Swir + i+1] # ��������� ��������� ����� ��������                   
                else: nextLiq = currLiq
    
                if(currLiq > liqCut):   # �������� ���������� � ��������� ������� 
                    outFile.write(" dynamic") 
                    if(nextLiq <= liqCut):                          
                        PBUstr = PBUstr + x.well + " " + str(times[i].tos) #��� �������� � ����� ������ ���
                        PBUstr = PBUstr + " " + str(currLiq) + " " + str(currLiqH) # ��������� � ����������� �����(������������) ��������
                        ###PBUstr = PBUstr + " " + str(currOil) + " " + str(currOilH) # ��������� � ����������� �����(������������) �����         #### ��������� ����� ������ ����� ####
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Sbhp + i]) #��������� �������� 
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Hbhp + i])  #����������� ��������
                else:
                    outFile.write(" static")                    
                    if(nextLiq > liqCut): 
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Sbhp + i])   #��������� ���������
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.Hbhp + i])   #����������� ���������
                        #PBUstr = PBUstr + " " + str(maxP)   #��������� ���������
                        #PBUstr = PBUstr + " " + str(maxPH)   #����������� ���������
                        #PBUstr = PBUstr + " " + str(times[i].tos)  # ����� ��������� ���                       
                        break # ��������� ���� ����� ��������� ������ ��� ��� ��������!
        #print(str(x.wt)," ", PBUstr) # ����� ���������� PBU � �������
        PBUstr = PBUstr + " " + str(maxP)   #��������� ���������
        PBUstr = PBUstr + " " + str(maxPH)   #����������� ���������
        PBUstr = PBUstr + " " + str(times[i].tos)  # ����� ��������� ���                       


        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n") #����� ���������� PBU � ����        
    outFile.close()
    wtOutFile.close()
    ###### ��������� ��������� ��������� ######
