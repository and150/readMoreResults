import constants
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
    outFile  = open(currDir+"\\"+rootName+".results", "w") # �������� ���� �������� ������������
    wtOutFile = open(currDir+"\\"+rootName+".WTout","w") # �������� ���� � ����������� ���
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # ��������� ������� ���������� ���        

    ####### ��������� ������ ��������� #######
    WTlist = GetWTlist(wtFileName, startDate)  #�������� ������ ��������� ������� (����� � ��������� ��������� ��� ����������� �� ��������� � �� �����, �� ���� ����������� ������ ��� ����� ���������)
      

    #### ����� ������� �������� � ������� Item
    tr = 0
    timetol = constants.TIMETOL
    liqCut = constants.LIQCUT
    PBUstr = ""
    T = len(times) # ���������� ������� RATE
    W = len(wellNames) # ���������� �������
    MZ = numsArray[5-1] # ���������� ����� � ��������� (���-�� ����� �� ���������, ����� ���� ���������� ��������
    V = constants.VEC + MZ*2*numsArray[55-1]       # ���������� �������� 

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


                currP  = ResArr[T*V*wi + T*2 + i]   #��������� �������� 
                currPH = ResArr[T*V*wi + T*5 + i]   #����������� �������� 
                if currP <= constants.PTOL or currPH <= constants.PTOL :
                    maxP = maxP
                    maxPH = maxPH
                else:
                    maxP = currP
                    maxPH = currPH


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
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*2 + i])   #��������� ���������
                        #PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T*5 + i])   #����������� ���������
                        #PBUstr = PBUstr + " " + str(maxP)   #��������� ���������
                        #PBUstr = PBUstr + " " + str(maxPH)   #����������� ���������
                        #PBUstr = PBUstr + " " + str(times[i])  # ����� ��������� ���                       
                        break # ��������� ���� ����� ��������� ������ ��� ��� ��������!
        #print(str(x.wt)," ", PBUstr) # ����� ���������� PBU � �������
        PBUstr = PBUstr + " " + str(maxP)   #��������� ���������
        PBUstr = PBUstr + " " + str(maxPH)   #����������� ���������
        PBUstr = PBUstr + " " + str(times[i])  # ����� ��������� ���                       

        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n") #����� ���������� PBU � ����        
    outFile.close()
    wtOutFile.close()
    ###### ��������� ��������� ��������� ######