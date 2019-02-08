import array
import struct
from getbindata import getBinData
import constants as cts
 
def readRATE (file, nums=[], times=[]):
    # nums[] - массив адресов показателей
    # nrate - количество временных шагов в файле rat

    class RatesHeader:
    # local class of 1-st time step header    
        def __init__(self, mnem="", units="", asname="", descr="", ASIND = [], ASDEPTH = []):    
            self.mnem = mnem     # Mnemonics
            self.units = units   # Units
            self.asname = asname # Associated name
            self.descr = descr   # Description
            self.ASIND = ASIND   # Associated index array (integer)
            # 1 – Associated x-index
            # 2 – Associated y-index
            # 3 – Associated z-index
            # 4 – Associated local grid
            # 5 – Associated component index
            # 6 – Associated fluid in place region
            # 7 – Associated second fluid in place region(for inter-region flows)
            # 8-16 are not currently used
            self.ASDEPTH = ASDEPTH # Associated depth array (real)
       
        def getData(self, bts): #!!! used constant byte positions 16 32 48 96 160 !!!
            self.mnem   = str(b''.join(struct.unpack('c'*16,bts[0:16])), 'utf-8') #block[0:16].decode("utf-8")    
            self.units  = str(b''.join(struct.unpack('c'*16,bts[16:32])), 'utf-8') #block[16:32].decode("utf-8")
            self.asname = str(b''.join(struct.unpack('c'*16,bts[32:48])), 'utf-8') #block[32:48].decode("utf-8")
            self.descr  = str(b''.join(struct.unpack('c'*48,bts[48:96])), 'utf-8') #block[48:96].decode("utf-8")
            self.ASIND = []
            self.ASDEPTH =[]
            for i in range(0,16):
                self.ASIND.append(int.from_bytes(bts[96+i*4:96+i*4+4],'little',signed='true'))
            for i in range(0,4):
                self.ASDEPTH.append(struct.unpack('f',bts[160+i*4:160+i*4+4])[0] )            

        def printRatesHeader(self):
            print(self.mnem)
            print(self.units)
            print(self.asname)
            print(self.descr)
            print(self.ASIND)
            print(self.ASDEPTH)    


    #######################################################
    #get data from num array
    ncompt = nums[2-1]  # Total number of components
    mw = nums[3-1]      # Maximum number of wells
    mwzone = nums[5-1]  # Maximum number of zones per well
    mwl = nums[7-1]     # Maximum number of well limits
    mg = nums[12-1]     # Maximum number of groups
    nphas = nums[16-1]  # Number of phases
    nstr = nums[21-1]   # Number of well streams
    NAQUIF = nums[33-1] # number of aquifers
    NIRAQU = nums[34-1]   # aqui
    nquant = nums[38-1]   # Number of additional rate quantities
    nqchar = nums[39-1]   # Number of characters associated with each rate quantity
    nqinte = nums[40-1]   # Number of integers associated with each rate quantity
    nqreal = nums[41-1]   # Number of reals associated with each rate quantity
    NIIRATE = nums[47-1]  # Number of items of IRATE data (21)    по нумс - 21
    NIIRPTR =  nums[48-1] # Number of items of IPPTR data (10)    по нумс - 12
    NIWRATE = nums[49-1]  # Number of items of WRATE data (22)    по нумс -23
    NIWMCMP = nums[50-1]  # Number of items of WMCMP data (4)   по файлу 4 
    NIWVCMP = nums[51-1]  # Number of items of WVCMP data (15)   по файлу 15
    NIWVLAY = nums[52-1]  # Number of items of WVLAY data (15)  по файлу 15
    NIGRVOL = nums[53-1]  # Number of items of GRVOL data (5) по файлу 5
    NIGVLAY = nums[54-1]  # Number of items of GVLAY data (18) по файлу 18
    IWVCMP = nums[55-1]   # Set to 1 if WVCMP written out, 0 otherwise
    IWVLAY = nums[56-1]   # Set to 1 if WVLAY written out, 0 otherwise   

    mstr = 5 # manual page 10

    #######################################################

    #READ HEADER DATA
    nbi =  cts.NBINT # number of bytes in integer
    nbf =  cts.NBFLOAT # number of bytes in float
    nbr =  cts.NBREAL # number of bytes in real
    V = cts.VEC + mwzone*2*IWVCMP # number of base vectors + number of layers* 2 (oil, water) if output by layers is present  
    Vbase = cts.VEC


    nrate = len(times)
    ResArr = [0]*nrate*V*mw  # [ ][timesteps][vectors][wells]  # array structure

    WNAMES = getBinData(file,'char16',mw,) #Well names   
    GNAMES = getBinData(file,'char16',mg,) #Group names  
    if (NAQUIF > 0): AQNAMES = getBinData(file,'char16',NAQUIF,) #Aquifer names  
    #print(WNAMES)    

    #массивы для хранения индексов исторических показателей                
    qoprh = [-1]*mw
    qwprh = [-1]*mw
    qbhph = [-1]*mw  
    qwirh = [-1]*mw      
    qwefa = [-1]*mw      

    #read quantity data (Mnemonics, Units, Associated names, Descriptions) !!!need check!!!!
    HARR = [] # массив заголовков векторов скважин (дополнительных вектров  miscellaneous???? 
    for i in range(0,nquant): 
        block = file.read(nqchar+nqinte*nbi+nqreal*nbr)
        rh = RatesHeader()
        rh.getData(block)
        HARR.append(rh)
        #print(HARR[i].mnem, HARR[i].units, HARR[i].asname, HARR[i].descr)  #debug output
        #print("|"+HARR[i].mnem.strip()+"| ",HARR[i].asname,"| ", HARR[i].descr)    #debug output

    for i in range(0,nquant): 
        for j in range(0,mw):                                         
            if (HARR[i].mnem.strip() == "woprh" and HARR[i].asname.strip() == WNAMES[j].strip()): qoprh[j] = i
            if (HARR[i].mnem.strip() == "wwprh" and HARR[i].asname.strip() == WNAMES[j].strip()): qwprh[j] = i
            if (HARR[i].mnem.strip() == "wwirh" and HARR[i].asname.strip() == WNAMES[j].strip()): qwirh[j] = i                   
            if (HARR[i].mnem.strip() == "wbhph" and HARR[i].asname.strip() == WNAMES[j].strip()): qbhph[j] = i              
            if (HARR[i].mnem.strip() == "wefa"  and HARR[i].asname.strip() == WNAMES[j].strip()): qwefa[j] = i              
            #print(HARR[i].mnem.strip() + " |" + HARR[i].asname.strip()+ "| "+ str(i) + " "+ str(j)+" |" +WNAMES[j].strip()+"| ")

    #### debug print ####
    #for j in range(0,mw):  # debug ouput
        #print(j, qoprh[j])      
        #print(j, qwprh[j])
        #print(j, qbhph[j])
        #print(j, qwefa[j])
        
    #print(qoprh, qwprh, qbhph, qwefa)
        #print(HARR[j].ASIND)
        #print(HARR[j].ASDEPTH)
        #HARR[j].printRatesHeader() #debug output                

    
    #READ RATES DATA    

    leng =(nstr+ncompt+1)*(nphas+2)+2*nstr+4*ncompt+2*ncompt*mwzone # General group data float*4 manual page 11

    #buffer arrays for data recording   
    iarr = array.array('l')
    farr = array.array('f')

    wtype = [0]*mw  # trigger of well type
    compArr = []  # array for well completion

    # расчет длины считываемого блока 
    wlen =  nbi*(NIIRATE + NIIRPTR*mwzone + mwl*2)  + nbf*(NIWRATE + 3*mstr + ncompt*3 + NIWMCMP*mwzone + ncompt*mwzone + IWVCMP*NIWVCMP*mwzone + IWVLAY*NIWVLAY*mwzone)
    glen =  nbi*1 + nbf*(leng + NIGRVOL*nstr + mw + NIGVLAY*mwzone)
    aqlen = nbf*NIRAQU
    totlen =  mw*wlen + mg*glen + aqlen*NAQUIF + nquant*nbr
    #print(wlen," ", glen, " ", aqlen, " ", nquant, " ",totlen)

    # by timesteps
    for n in range(0,nrate): 
       
        # чтение записи для одного временного шага
        line = file.read(totlen )
        #print(struct.unpack('i'*tt,line)) # debug output

        #if n%50==0:
        #    print("STEP ",n)     # debug output                      
        #print("STEP ",n)
        
        # READ WELL RATES        
        s = 0
        f = 0
        # by wells
        for j in range(0,mw):                                      

            # irate       # Integer well data    int*4
            del iarr[:]                         
            s = j*wlen 
            f = s + NIIRATE*nbi
            iarr.frombytes(line[s:f])              
            wtype[j] = iarr[7]  #wtype = buffArr[7]          # запоминаем текущий тип скважины (1 - добывающая, -1 - нагнетательная)

        
            # irptr       # Completion location data          int*4
            del iarr[:]
            s = f 
            f = s + NIIRPTR*mwzone*nbi
            iarr.frombytes(line[s:f])
            compArr = iarr[mwzone*3:mwzone*4] # запоминаем массив номеров текущих активных соединений


            # irlim       # Well constraint information       int*4
            #line.seek(mwl*2*intSize,1)            


            #wrate     # Miscellaneous well data          float*4
            del farr[:]
            s = f + mwl*2*nbi
            f = s + NIWRATE*nbf
            farr.frombytes(line[s:f])      
            #print(farr)
            ResArr[nrate*V*j + nrate* cts.Sbhp + n] = farr[3]        # записываем забойное давление, скорректированное на ссылочную глубину            
           

            # wrvol    # Well volume rates and totals  float*4
            del farr[:]
            s = f
            f = s + 3*mstr*nbf
            farr.frombytes(line[s:f])   
            #print(farr)
            ResArr[nrate*V*j + nrate* cts.Sopr + n] = farr[0]   # записываем дебит нефти
            ResArr[nrate*V*j + nrate* cts.Sopt + n] = farr[5]   # записываем накопленную нефть для добывающих
            ResArr[nrate*V*j + nrate* cts.Swpt + n] = farr[7]   # записываем накопленную воду  для добывающих
            if(wtype[j] == 1): 
                ResArr[nrate*V*j + nrate* cts.Swpr + n] = farr[2]   # записываем дебит воды для добывающих
            elif(wtype[j]==-1):
                ResArr[nrate*V*j + nrate* cts.Swir + n] = farr[1]   # приемистость для нагнетательных  
                ResArr[nrate*V*j + nrate* cts.Swit + n] = farr[11]   # записываем накопленную закачку для нагнетательных 
           

            # wrms         # Well molar rates and totals      float*4
            #line.seek(ncompt*3*nbf,1)        
            

            # wmcmp        # Miscellaneous completion data    float*4
            #line.seek(NIWMCMP*mwzone*nbf,1)            


            # wrcmp        # Completion molar flow rates      float*4
            #file.seek(ncompt*mwzone*nbf,1)            


            # wvcmp        # Completion volume flows float*4
            if IWVCMP == 1:                       
                del farr[:]
                s = f + ncompt*3*nbf + NIWMCMP*mwzone*nbf + ncompt*mwzone*nbf
                f = s + NIWVCMP*mwzone*nbf
                farr.frombytes(line[s:f])
                for kk in range(0,mwzone): # итерация по слоям модели
                   if compArr[kk] !=0:
                      ResArr[nrate*V*j + nrate*(Vbase + compArr[kk]-1) + n] = farr[kk]  # записываем дебит нефти по перфорациям                   
                      ResArr[nrate*V*j + nrate*(Vbase + mwzone + compArr[kk] - 1) + n] = farr[kk + 2*mwzone] # записываем дебит воды(приемистость) по перфорациям



           # wvlay  # Well layer volume flows float*4

           #if IWVLAY == 1:                      
           #     for k in range(0,NIWVLAY):       
           #         line.seek(mwzone*floatSize,1) 

        #READ GROUP AND FIP DATA
        #line.seek(mg*(1*intSize + leng*floatSize + NIGRVOL*nstr*floatSize + mw*floatSize + NIGVLAY*mwzone*floatSize ),1)
        #for k in range(0,mg): 
        #    file.seek(1*intSize,1)             #sep          # separator flag                    int*4
        #    file.seek(leng*floatSize,1)        #gdata        # General group data               float*4    
        #    for k in range(0,NIGRVOL):         #grvol        # General group volumes            float*4
        #        file.seek(nstr*floatSize, 1)   #grvol
        #    file.seek(mw*floatSize,1)          #wfr          # Fraction for each well in group  float*4
        #    for k in range(0,NIGVLAY):         #gvlay        # Group layer volume flows         float*4 
        #        file.seek(mwzone*floatSize,1)  #gvlay

        #READ AQUIFER DATA (IF ANY)
        #line.seek(NAQUIF*NIRAQU*floatSize, 1)
        #for k in range(0,NAQUIF): 
        #    file.seek(NIRAQU*floatSize, 1)    #aquifer    !!!!!not tested on model with aquifer, might be a source of errors!!!!!

        #READ QUANTITY DATA (дополнительные вектора, указанные в заголовке)
        del farr[:]
        s = mw*wlen + mg*glen + NAQUIF*aqlen 
        f = s + nquant*nbr        
        farr.frombytes(line[s:f]) #buffArr = getBinData(file,'float',nquant,)
        #print(farr)
        # считывание дополнительных массивов 
        for j in range(0,mw):
            if(qoprh[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.Hopr + n] = farr[qoprh[j]] # get history oil rates if any
            if(qwprh[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.Hwpr + n] = farr[qwprh[j]] # get history water rates if any
            if(qwirh[j] >= 0 and wtype[j] == -1 ): ResArr[nrate*V*j + nrate*cts.Hwir + n] = farr[qwirh[j]]  # ВНИМАНИЕ, если есть приемистость, то переписываем ее вместо дебита воды!!!!  как-то сомнительно.... но на тестовой модели работает, а на реальной нет....                                                
            if(qbhph[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.Hbhp + n] = farr[qbhph[j]] # get history bhp if any 
            if(qwefa[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.Hwefa + n] = farr[qwefa[j]] # get history wefa if any 
            # расчет исторических накопленных показателей
            if(n==0):
                ResArr[nrate*V*j + nrate*cts.Hopt + n] = 0 + ResArr[nrate*V*j + nrate*cts.Hopr + n] * times[n].tos / 1000
                ResArr[nrate*V*j + nrate*cts.Hwpt + n] = 0 + ResArr[nrate*V*j + nrate*cts.Hwpr + n] * times[n].tos / 1000
                ResArr[nrate*V*j + nrate*cts.Hwit + n] = 0 + ResArr[nrate*V*j + nrate*cts.Hwir + n] * times[n].tos / 1000
            else:
                ResArr[nrate*V*j + nrate*cts.Hopt + n] = ResArr[nrate*V*j + nrate*cts.Hopt + n-1] + ResArr[nrate*V*j + nrate*cts.Hopr + n] * (times[n].tos - times[n-1].tos )/ 1000
                ResArr[nrate*V*j + nrate*cts.Hwpt + n] = ResArr[nrate*V*j + nrate*cts.Hwpt + n-1] + ResArr[nrate*V*j + nrate*cts.Hwpr + n] * (times[n].tos - times[n-1].tos )/ 1000
                ResArr[nrate*V*j + nrate*cts.Hwit + n] = ResArr[nrate*V*j + nrate*cts.Hwit + n-1] + ResArr[nrate*V*j + nrate*cts.Hwir + n] * (times[n].tos - times[n-1].tos )/ 1000


            
        # возвращаем массив прочиатнных данных, повременная запись конвертирована в массив векторов
    #return Items
    return (ResArr, WNAMES)


