#-*- coding:utf-8 -*-
from getbindata import getBinData


def readMISC(input_file):
# there in not EOS-parameters reading in the current release    
    #######################################################   
    
    #MISC section  
    sect_name = getBinData(input_file,'char',4,) #[0]    # section name                                                  #record of 4 char
    nbytes1 = getBinData(input_file,'int',1,)      # number of bytes in the section                                  #record of 1 int    
    method = getBinData(input_file,'int',1,)       # Method XYZ, X - major version, Y - minor version, Z - revision   #record of 1 int    
    ni = getBinData(input_file,'int',1,)           # Ni = number of values in next recort (i - integer)               #record of 1 int       
    tArr =  getBinData(input_file,'int',ni,)       # tArr - temporary array # gets Date of run, units & case flag

    ####### get start date into global variable
    SDAT = []
    SDAT.append(tArr[0])
    SDAT.append(tArr[1])
    SDAT.append(tArr[2])

    #print(f"sect_name={sect_name}, nbytes1={nbytes1}, method={method}, ni={ni}, tArr={tArr}") # debug

    #######################################################
    #PRHD section    
    sect_name =  getBinData(input_file,'char',4,)      # section name                        #record of 4 char
    nbytes2 = getBinData(input_file,'int',1,)           # number of bytes in the section      #record of 1 int    
    nph = getBinData(input_file,'int',1,)               # nph lengh of run headers (75)       #record of 1 int
    nrv = getBinData(input_file,'int',1,)               # nrv length of revision date (30)    #record of 1 int    
    
    revDate =  ''.join(getBinData(input_file,'char',nrv,))  # revision date                       #record of nrv chars      
    #prHeadI = ''.join(getBinData(input_file,'char',nph,))   # programm header I                   #record of nph chars     
    #prHeadII = ''.join(getBinData(input_file,'char',nph,))  # programm header II                  #record of nph chars
    #skip headers
    prHeadI = input_file.read(nph)         # programm header I                   #record of nph chars    
    prHeadII = input_file.read(nph)        # programm header II                  #record of nph chars
    
    #revDate = getBinData(input_file,'int',nrv,)          # revision date                       #record of nrv chars 
    #prHeadI = getBinData(input_file,'int',nph,)          # programm header I                   #record of nph chars    
    #prHeadII = getBinData(input_file,'int',nph,)         # programm header II                  #record of nph chars

    #print(f"sect_name={sect_name}, nbytes2={nbytes2}, nph={nph}, nrv={nrv}, revDate={revDate}, prHeadI={prHeadI}, prHeadII={prHeadII}") # debug
   
    #######################################################
    #NUMB section
    sect_name = getBinData(input_file,'char',4,)         # section name                                #record of 4 char  
    nbnumb = getBinData(input_file,'int',1,)             # number of bytes in the section              #record of 1 int  
    nn = getBinData(input_file,'int',1,)                 # nn dimension of nums array                  #record of 1 int    
    nums = []                                    # array of numbers for RATE and ARRAY input_files   #record of nn int
    for i in range(0,nn):
        nums.append(getBinData(input_file,'int',1,))

    #print(f"sect_name={sect_name}, nbnumb={nbnumb}, nn={nn}, nums={nums}") # debug
    
    #######################################################
    #PROP section    
    sect_name = getBinData(input_file,'char',4,)           # section name                               #record of 4 char        
    nbprop = getBinData(input_file,'int',1,)             # number of bytes in prop section            #record of 1 int       
    method = getBinData(input_file,'int',1,)             # for upward compatibility                   #record of 1 int
    nc = getBinData(input_file,'int',1,)                 # number of components                       #record of 1 int
    nl = getBinData(input_file,'int',1,)                 # number of lumped components                #record of 1 int
    nstd = getBinData(input_file,'int',1,)               # number of standard compositions            #record of 1 int
    ms = getBinData(input_file,'int',1,)                 # maximum number of standard compositions    #record of 1 int
    mp = getBinData(input_file,'int',1,)                 # maximum number of phases                   #record of 1 int
   
    #print(f"sect_name={sect_name}, nbprop={nbprop}, method={method}, nc={nc}, nl={nl}, nstd={nstd}, ms={ms}, mp={mp}") # debug

    #records of above dimensions
    PHASNM = getBinData(input_file,'char',mp*16,)     # Names of fluid phases
    COMPNM = getBinData(input_file,'char',nc*16,)     # Names of components
    IDPHAS = getBinData(input_file,'int',mp,)        # Indicates if phase ip is present (1-oil, 2-gas, 3-water, 4-other)
    IDLOCX = getBinData(input_file,'int',nc*mp,)     # Indicates if components in phase (0-not, -1 if only component in phase)
    IPCPHZ = getBinData(input_file,'int',mp,)        # Indicates use of cap press for phase
    AMOLWT = getBinData(input_file,'float',nc,)       # Molecular weights
    VLIQSC = getBinData(input_file,'float',nc)       # Molar liquid volume of components
    VGASSC = getBinData(input_file,'float',nc)       # Molar vapor volume of components
    LUMPNM = getBinData(input_file,'char',nl*16,)     # Names of lumped components
    LUMPCP = getBinData(input_file,'int',nc*nl,)     # Is component in lumped component
    STDCNM = getBinData(input_file,'char',ms*16,)     # Names of standard compositions
    STDCMP = getBinData(input_file,'float',nc*ms,)    # Standard compositions
    SURFDENS = getBinData(input_file,'float',3,)      # Standard compositions    

    #print(f"PHASNM ={PHASNM} \nCOMPNM ={COMPNM} \nIDPHAS ={IDPHAS} \nIDLOCX ={IDLOCX} \nIPCPHZ ={IPCPHZ} \nAMOLWT ={AMOLWT} \nVLIQSC ={VLIQSC} \nVGASSC ={VGASSC} \nLUMPNM ={LUMPNM} \nLUMPCP ={LUMPCP} \nSTDCNM ={STDCNM} \nSTDCMP ={STDCMP} \nSURFDENS = {SURFDENS}") # debug

    #######################################################
    #FLUI section
    sect_name = getBinData(input_file,'char',4,)            # section name                        #record of 4 char            
    nbflui = getBinData(input_file,'int',1,)             # nbflui                              #record of 1 int            
    eos = getBinData(input_file,'int',1,)                # for black oil eos=0                 #record of 1 int    

    #print(f"sect_name={sect_name}, nbflui={nbflui}, eos={eos}") # debug

    #if(eos == 1):
        # !!!!!!!!!!!!!!!!! TODO realize EOS section reading  need section to read EoS parameters ()
    

    #######################################################
    #LIMI section
    sect_name = getBinData(input_file,'char',4,)   # section name                       #record of 4 char      
    nblimi = getBinData(input_file,'int',1,)        # nblimi                             #record of 1 int
    nlim = getBinData(input_file,'int',1,)          #nlim                                #record of 1 int
    mstrp = getBinData(input_file,'int',1,)         #max streams + 1                     #record of 1 int
    mlim = getBinData(input_file,'int',1,)          #max limits                          #record of 1 int
    method = getBinData(input_file,'int',1,)        #XXX for upwards compatibility       #record of 1 int   

    #print(f"sect_name={sect_name}, nblimi={nblimi}, nlim={nlim}, mstrp={mstrp}, mlim={mlim}, method={method}")

    #records of above dimensions    
    WLIMIT = getBinData(input_file,'char',mlim*16) # Names of well limits
    IDXVAR = getBinData(input_file,'int',mlim)  # A value of 6 indicates a rate limit, a value <6 indicates a ration limit
    IDSIGN = getBinData(input_file,'int',mlim)  # Sign associated with the limit
    WLIMITW = getBinData(input_file,'float',mstrp*mlim) # Well limits weights
    
    #print(f"WLIMIT={WLIMIT} \nIDXVAR={IDXVAR} \nIDSIGN={IDSIGN}, \nWLIMITW={WLIMITW}") # debug
    
    #######################################################
    #SEPA section
    #sect_name = getBinData(input_file,'char',4,)      # section name                        #record of 4 char    
    sepa_nums = {'sect_name':['','char',4], 
                 'nbsepa':[0,'int',1], 
                 'XXX':[0,'int',1], 
                 'nsep':[0,'int',1], 
                 'nistr':[0,'int',1], 
                 'npstr':[0,'int',1], 
                 'mstr':[0,'int',1], 
                 'msep':[0,'int',1], 
                 'mcomp':[0,'int',1]}
    for item in sepa_nums:
        sepa_nums[item][0] = getBinData(input_file, sepa_nums[item][1],sepa_nums[item][2],)
        #print(f"{item} = {sepa_nums[item][0]}") # debug

    sepa_vals = {   'WSEPNM': ['', 'char', sepa_nums['msep'][0]*16],
                    'WPFLNM': ['', 'char', sepa_nums['mstr'][0]*16],
                    'WIFLNM': ['', 'char', sepa_nums['mstr'][0]],
                    'IPSTRM': ['', 'int',  sepa_nums['mstr'][0]],
                    'NSPLST': ['', 'int',  sepa_nums['msep'][0]],
                    'IEKVAR': ['', 'int',  sepa_nums['msep'][0]],
                    'IEOSDN': ['', 'int',  sepa_nums['msep'][0]],
                    'ISTEMP': ['', 'int',  sepa_nums['msep'][0]],
                    'IPHSTM': ['', 'int',  sepa_nums['mstr'][0]],
                    'SPTEMP': ['', 'float', sepa_nums['msep'][0]],
                    'SPRESS': ['', 'float', sepa_nums['msep'][0]],
                    'VFSEPR': ['', 'float', sepa_nums['msep'][0]],
                    'FISTRM': ['', 'float', sepa_nums['mcomp'][0]*sepa_nums['mstr'][0]],
                    'FPSTRM': ['', 'float', sepa_nums['mcomp'][0]*sepa_nums['mstr'][0]],
                    'ZFSEPR': ['', 'float', sepa_nums['msep'][0]*2],
                    'EKSEPR': ['', 'float', sepa_nums['mcomp'][0]*sepa_nums['msep'][0]] }

    for item in sepa_vals:
        sepa_vals[item][0] = getBinData(input_file, sepa_vals[item][1],sepa_vals[item][2],)
        #print(f"{item} = {sepa_vals[item][0]}") # debug


    #nbsepa = getBinData(input_file,'int',1,)[0]  # nbsepa                              #record of 1 int
    #XXX = getBinData(input_file,'int',1,)[0]     # method (for upward compatibility)
    #nsep = getBinData(input_file,'int',1,)[0]    # number of separator specifications
    #nistr = getBinData(input_file,'int',1,)[0]   # number injection streams
    #npstr = getBinData(input_file,'int',1,)[0]   # number production streams
    #mstr = getBinData(input_file,'int',1,)[0]    # maximum streams
    #msep = getBinData(input_file,'int',1,)[0]    # maximum separators
    #mcomp = getBinData(input_file,'int',1,)[0]   # maximum components
    
    #records of above dimensions  
    #WSEPNM  = getBinData(input_file,'char16',msep,)         # Separator names
    #WPFLNM  = getBinData(input_file,'char16',mstr,)         # Production streams
    #WIFLNM  = getBinData(input_file,'char',mstr,)         # Injection streams
    #IPSTRM  = getBinData(input_file,'int',mstr,)          # Is stream oil or gas? (1-Oil, 2-Gas)
    #NSPLST  = getBinData(input_file,'int',msep,)          # Index of last sep in description
    #IEKVAR  = getBinData(input_file,'int',msep,)          # 0: Use fixed K-values; 1: Use EoS
    #IEOSDN  = getBinData(input_file,'int',msep,)          # 0: Fixed density; 1: EoS density
    #ISTEMP  = getBinData(input_file,'int',msep,)          # Temperature index for sep
    #IPHSTM  = getBinData(input_file,'int',mstr,)          # Phase split indicator
    #SPTEMP  = getBinData(input_file,'float',msep,)        # Separator temperature
    #SPRESS  = getBinData(input_file,'float',msep,)        # Separator pressure
    #VFSEPR  = getBinData(input_file,'float',msep,)        # Vapour fraction
    #FISTRM  = getBinData(input_file,'float',mcomp*mstr,)  # Fraction of component in inj stream
    #FPSTRM  = getBinData(input_file,'float',mcomp*mstr,)  # Fraction of component in prod stream
    #ZFSEPR  = getBinData(input_file,'float',2*msep,)      # Liquid and vapour Z-factors
    #EKSEPR  = getBinData(input_file,'float',mcomp*msep,)  # Kvalues for separators
      
    #### debug print ####
    #print(sect_name.decode("utf-8"))    
    #print(nbsepa)
    #print()
    #### end of debug print #### 

    #######################################################
    #RESTART section    
    sect_name = getBinData(input_file,'char',4,)        # section name                        #record of 4 char    
    nbrest = getBinData(input_file,'int',1,)   # nbrest
    niblock = getBinData(input_file,'int',1,)  # niblock
    
    nrest= getBinData(input_file,'int',1,)     # number of restarts
    ncpr = getBinData(input_file,'int',1,)     # number of characters/restart
    nipr = getBinData(input_file,'int',1,)     # number of integers/restart
    nfpr = getBinData(input_file,'int',1,)     # number of floats/restart
           
    #print(f"sect_name={sect_name}, nbrest={nbrest}, niblock={niblock}, nrest={nrest}, ncpr={ncpr}, nipr={nipr}, nfpr={nfpr}") # debug

    NAMEOFRUN = ""
    RESTSTEP = []
    STARTTIME = []
    for i in range (0,nrest):
        NAMEOFRUN = getBinData(input_file,'char',ncpr*16,)
        RESTSTEP = getBinData(input_file,'int',nipr,)
        STARTTIME =getBinData(input_file,'float',nfpr,)

    #print(f"NAMEOFRUN={NAMEOFRUN}, RESTSTEP = {RESTSTEP}, STARTTIME = {STARTTIME}") # debug
   
    return (SDAT, nums) # returns STARTDATE and NUMS array 


