#-*- coding:utf-8 -*-
import array, struct, sys
from getbindata import getBinData
import constants as cts
import tracemalloc


#from pympler.tracker import SummaryTracker
#tracker = SummaryTracker()
#tracker.print_diff()

def readRATE (input_file, nums=[], times=[]):
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


    #print(f"\nin the beginning of the module")
    #tracker.print_diff()

    tracemalloc.start()


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
    NIIRATE = nums[47-1]  # Number of items of IRATE data (21)
    NIIRPTR =  nums[48-1] # Number of items of IPPTR data (10)    by nums - 12
    NIWRATE = nums[49-1]  # Number of items of WRATE data (22)    by nums -23
    NIWMCMP = nums[50-1]  # Number of items of WMCMP data (4)
    NIWVCMP = nums[51-1]  # Number of items of WVCMP data (15)
    NIWVLAY = nums[52-1]  # Number of items of WVLAY data (15)
    NIGRVOL = nums[53-1]  # Number of items of GRVOL data (5)
    NIGVLAY = nums[54-1]  # Number of items of GVLAY data (18)
    IWVCMP = nums[55-1]   # Set to 1 if WVCMP written out, 0 otherwise
    IWVLAY = nums[56-1]   # Set to 1 if WVLAY written out, 0 otherwise   

    mstr = 5 # manual page 10


    #READ HEADER DATA
    nbi =  cts.NBINT # number of bytes in integer
    nbf =  cts.NBFLOAT # number of bytes in float
    nbr =  cts.NBREAL # number of bytes in real
    V = cts.VEC + mwzone*2*IWVCMP # number of base vectors + number of layers* 2 (oil, water) if output by layers is present  
    Vbase = cts.VEC

    nrate = len(times)
    ResArr = [0]*nrate*V*mw  # [ ][timesteps][vectors][wells]  # array structure
    perf_array = [] # array of well completions by timesteps and by well numbers [timestep, well_number, [i-index], [j-index], [k-index]]

    WNAMES = []
    for i in range(mw): 
        WNAMES.append(getBinData(input_file,'char',16,))   #Well names   
    #print(WNAMES) # debug

    GNAMES = []
    for i in range(mg):
        GNAMES.append(getBinData(input_file,'char',16,))   #Group names  
    #print(GNAMES) # debug

    if (NAQUIF > 0): 
        AQNAMES = []
        for i in range(NAQUIF):
            AQNAMES.append(getBinData(input_file,'char',16,)) #Aquifer names  

    # history arrays
    qoprh = [-1]*mw
    qwprh = [-1]*mw
    qbhph = [-1]*mw  
    qwirh = [-1]*mw      
    qwefa = [-1]*mw      
    qthph = [-1]*mw
    wPI4 = [-1]*mw

    #read quantity data (Mnemonics, Units, Associated names, Descriptions) !!!need check!!!!
    HARR = [] # array of vectors' headers (additional vectors miscellaneous
    for i in range(0,nquant): 
        block = input_file.read(nqchar+nqinte*nbi+nqreal*nbr)
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
            if (HARR[i].mnem.strip() == "wthph" and HARR[i].asname.strip() == WNAMES[j].strip()): qthph[j] = i              
            if (HARR[i].mnem.strip() == "wPI4" and HARR[i].asname.strip() == WNAMES[j].strip()): wPI4[j] = i              
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
    i_comp = []  # i-index of well completions
    j_comp = []  # j-index of well completions
    k_comp = []  # k-index of well completions

    # calculation of a length of input data block
    wlen =  nbi*(NIIRATE + NIIRPTR*mwzone + mwl*2)  + nbf*(NIWRATE + 3*mstr + ncompt*3 + NIWMCMP*mwzone + ncompt*mwzone + IWVCMP*NIWVCMP*mwzone + IWVLAY*NIWVLAY*mwzone)
    glen =  nbi*1 + nbf*(leng + NIGRVOL*nstr + mw + NIGVLAY*mwzone)
    aqlen = nbf*NIRAQU
    totlen =  mw*wlen + mg*glen + aqlen*NAQUIF + nquant*nbr
    #print(wlen," ", glen, " ", aqlen, " ", nquant, " ",totlen)

    #print(f"\nbefore entering timestep cycle")
    #tracker.print_diff()



    # by timesteps
    for n in range(0,nrate): 
       
        # reads one timestep
        line = input_file.read(totlen )
        #print(f"{n}  --  {sys.getsizeof(line)}")

        if n%100==0:  # debug 
        #    print("STEP ",n)  
        #    tracker.print_diff()

            print("\n---============================-----------------------------------------------------------\n")
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            for stat in top_stats[:10]:
                print(stat)

        
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
            wtype[j] = iarr[7]  #wtype = buffArr[7]          # remember the type of the well (1 - producer, -1 - injector)

        
            # irptr       # Completion location data          int*4
            del iarr[:]
            s = f 
            f = s + NIIRPTR*mwzone*nbi
            iarr.frombytes(line[s:f])
            block_index = iarr[mwzone*0:mwzone*1]
            i_comp = iarr[mwzone*1:mwzone*2] #  get i-index of the current flowing connections
            j_comp = iarr[mwzone*2:mwzone*3] #  get j-index of the current flowing connections
            k_comp = iarr[mwzone*3:mwzone*4] #  get k-index of the current flowing connections
            lgr_index = iarr[mwzone*4:mwzone*5] # 0 - global grid, else LGR index
            perf_array.append([n,j,[*i_comp], [*j_comp], [*k_comp], [*lgr_index]]) # append current well connections
            #print(f"timestep={n}, wellnumber= {j}, block_index={block_index}, comps={[i_comp, j_comp, k_comp]}") # debug


            # irlim       # Well constraint information       int*4
            #line.seek(mwl*2*intSize,1)            


            #wrate     # Miscellaneous well data          float*4
            del farr[:]
            s = f + mwl*2*nbi
            f = s + NIWRATE*nbf
            farr.frombytes(line[s:f])      
            #print(farr)
            ResArr[nrate*V*j + nrate* cts.i_d['Sbhp'] + n] = farr[3]        # get bottom hole pressure referenced
            ResArr[nrate*V*j + nrate* cts.i_d['Sthp'] + n] = farr[9]        # get tubing head pressure
           

            # wrvol    # Well volume rates and totals  float*4
            del farr[:]
            s = f
            f = s + 3*mstr*nbf
            farr.frombytes(line[s:f])   
            #print(farr)
            ResArr[nrate*V*j + nrate* cts.i_d['Sopr'] + n] = farr[0]   # get oil rate
            ResArr[nrate*V*j + nrate* cts.i_d['Sopt'] + n] = farr[5]   # get cumulative oil for producers
            ResArr[nrate*V*j + nrate* cts.i_d['Swpt'] + n] = farr[7]   # get cumulative water for producers
            if(wtype[j] == 1): 
                ResArr[nrate*V*j + nrate* cts.i_d['Swpr'] + n] = farr[2]   # get water rate for producers
            elif(wtype[j]==-1):
                ResArr[nrate*V*j + nrate* cts.i_d['Swir'] + n] = farr[1]   # injectivity (water rate) for injectors
                ResArr[nrate*V*j + nrate* cts.i_d['Swit'] + n] = farr[11]   # get cumulative injection for injectors
           

            # wrms         # Well molar rates and totals      float*4
            #line.seek(ncompt*3*nbf,1)        
            

            # wmcmp        # Miscellaneous completion data    float*4
            #line.seek(NIWMCMP*mwzone*nbf,1)            


            # wrcmp        # Completion molar flow rates      float*4
            #input_file.seek(ncompt*mwzone*nbf,1)            


            # wvcmp        # Completion volume flows float*4
            if IWVCMP == 1:                       
                del farr[:]
                s = f + ncompt*3*nbf + NIWMCMP*mwzone*nbf + ncompt*mwzone*nbf
                f = s + NIWVCMP*mwzone*nbf
                farr.frombytes(line[s:f])
                for kk in range(0,mwzone): # iteration by grid layers
                   if k_comp[kk] !=0:
                      ResArr[nrate*V*j + nrate*(Vbase + k_comp[kk]-1) + n] = farr[kk]  # get connection oil rate
                      ResArr[nrate*V*j + nrate*(Vbase + mwzone + k_comp[kk] - 1) + n] = farr[kk + 2*mwzone] # get connection water rate (injection rate)



           # wvlay  # Well layer volume flows float*4

           #if IWVLAY == 1:                      
           #     for k in range(0,NIWVLAY):       
           #         line.seek(mwzone*floatSize,1) 

        #READ GROUP AND FIP DATA
        #line.seek(mg*(1*intSize + leng*floatSize + NIGRVOL*nstr*floatSize + mw*floatSize + NIGVLAY*mwzone*floatSize ),1)
        #for k in range(0,mg): 
        #    input_file.seek(1*intSize,1)             #sep          # separator flag                    int*4
        #    input_file.seek(leng*floatSize,1)        #gdata        # General group data               float*4    
        #    for k in range(0,NIGRVOL):         #grvol        # General group volumes            float*4
        #        input_file.seek(nstr*floatSize, 1)   #grvol
        #    input_file.seek(mw*floatSize,1)          #wfr          # Fraction for each well in group  float*4
        #    for k in range(0,NIGVLAY):         #gvlay        # Group layer volume flows         float*4 
        #        input_file.seek(mwzone*floatSize,1)  #gvlay

        #READ AQUIFER DATA (IF ANY)
        #line.seek(NAQUIF*NIRAQU*floatSize, 1)
        #for k in range(0,NAQUIF): 
        #    input_file.seek(NIRAQU*floatSize, 1)    #aquifer    !!!!!not tested on model with aquifer, might be a source of errors!!!!!

        #READ QUANTITY DATA (miscellaneous vecors named in headers)
        del farr[:]
        s = mw*wlen + mg*glen + NAQUIF*aqlen 
        f = s + nquant*nbr        
        farr.frombytes(line[s:f]) #buffArr = getBinData(input_file,'float',nquant,)
        #print(farr)
        # read miscellaneous vectors (history vectors)
        for j in range(0,mw):
            if(qoprh[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.i_d['Hopr'] + n] = farr[qoprh[j]] # get history oil rates if any
            if(qwprh[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.i_d['Hwpr'] + n] = farr[qwprh[j]] # get history water rates if any
            if(qwirh[j] >= 0 and wtype[j] == -1 ): ResArr[nrate*V*j + nrate*cts.i_d['Hwir'] + n] = farr[qwirh[j]]  # ACHTUNG!!, if there is injection it is written instead of water rate
            if(qbhph[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.i_d['Hbhp'] + n] = farr[qbhph[j]] # get history bhp if any 
            if(qwefa[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.i_d['Hwefa'] + n] = farr[qwefa[j]] # get history wefa if any 
            if(qthph[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.i_d['Hthp'] + n] = farr[qthph[j]] # get history bhp if any 
            if(wPI4[j] >= 0 ): ResArr[nrate*V*j + nrate*cts.i_d['wPI4'] + n] = farr[wPI4[j]] # get wPI4 if any
            # calculation of history cumulatives
            if(n==0):
                ResArr[nrate*V*j + nrate*cts.i_d['Hopt'] + n] = 0 + ResArr[nrate*V*j + nrate*cts.i_d['Hopr'] + n] * times[n].tos / 1000
                ResArr[nrate*V*j + nrate*cts.i_d['Hwpt'] + n] = 0 + ResArr[nrate*V*j + nrate*cts.i_d['Hwpr'] + n] * times[n].tos / 1000
                ResArr[nrate*V*j + nrate*cts.i_d['Hwit'] + n] = 0 + ResArr[nrate*V*j + nrate*cts.i_d['Hwir'] + n] * times[n].tos / 1000
            else:
                ResArr[nrate*V*j + nrate*cts.i_d['Hopt'] + n] = ResArr[nrate*V*j + nrate*cts.i_d['Hopt'] + n-1] + ResArr[nrate*V*j + nrate*cts.i_d['Hopr'] + n] * (times[n].tos - times[n-1].tos )/ 1000
                ResArr[nrate*V*j + nrate*cts.i_d['Hwpt'] + n] = ResArr[nrate*V*j + nrate*cts.i_d['Hwpt'] + n-1] + ResArr[nrate*V*j + nrate*cts.i_d['Hwpr'] + n] * (times[n].tos - times[n-1].tos )/ 1000
                ResArr[nrate*V*j + nrate*cts.i_d['Hwit'] + n] = ResArr[nrate*V*j + nrate*cts.i_d['Hwit'] + n-1] + ResArr[nrate*V*j + nrate*cts.i_d['Hwir'] + n] * (times[n].tos - times[n-1].tos )/ 1000

            
        # return array of data read, timesteps converted to array of vectors
    #return Items

    #print(f"\nbefore input_file.close()")
    #tracker.print_diff()

    input_file.close()
    #[print(f"timestep={item[0]} well_num={item[1]} i-index={item[2]} j-index={item[3]} k-index={item[4]}") for item in perf_array] # debug

    #print(f"\nbefore return")
    #tracker.print_diff()

    return (ResArr, WNAMES, perf_array)
