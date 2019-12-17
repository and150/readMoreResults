#-*- coding:utf-8 -*-
from getbindata import getBinData


def readMISC(file):
# there in not EOS-parameters reading in the current release    
    #######################################################   
    
    #MISC section  
    sect_name = getBinData(file,'char4',1,)[0]    # section name                                                  #record of 4 char
    nbytes1 = getBinData(file,'int',1,)[0]      # number of bytes in the section                                  #record of 1 int    
    method = getBinData(file,'int',1,)[0]       # Method XYZ, X - major version, Y - minor version, Z - revision   #record of 1 int    
    ni = getBinData(file,'int',1,)[0]           # Ni = number of values in next recort (i - integer)               #record of 1 int       
    tArr =  getBinData(file,'int',ni,1)       # tArr - temporary array # gets Date of run, units & case flag

    ####### get start date into global variable
    SDAT = []
    SDAT.append(tArr[0])
    SDAT.append(tArr[1])
    SDAT.append(tArr[2])

    ### debug print ####
    #print(sect_name.decode("utf-8"))
    #print(nbytes1)
    #print(method, ni)
    #print("date of run: ",tArr[0:3]) # Date of run
    #print("units flag: ",tArr[3]) # units 1
    #print("case flag: ",tArr[4])
    #print()
    ## end of debug print ####

    #######################################################
    #PRHD section    
    sect_name =  getBinData(file,'char4',1,)[0]      # section name                        #record of 4 char
    nbytes2 = getBinData(file,'int',1,)[0]           # number of bytes in the section      #record of 1 int    
    nph = getBinData(file,'int',1,)[0]               # nph lengh of run headers (75)       #record of 1 int
    nrv = getBinData(file,'int',1,)[0]               # nrv length of revision date (30)    #record of 1 int    
    
    revDate =  ''.join(getBinData(file,'char',nrv,))  # revision date                       #record of nrv chars      
    #prHeadI = ''.join(getBinData(file,'char',nph,))   # programm header I                   #record of nph chars     
    #prHeadII = ''.join(getBinData(file,'char',nph,))  # programm header II                  #record of nph chars
    #skip headers
    prHeadI = file.read(nph)         # programm header I                   #record of nph chars    
    prHeadII = file.read(nph)        # programm header II                  #record of nph chars
    
    #revDate = getBinData(file,'int',nrv,)          # revision date                       #record of nrv chars 
    #prHeadI = getBinData(file,'int',nph,)          # programm header I                   #record of nph chars    
    #prHeadII = getBinData(file,'int',nph,)         # programm header II                  #record of nph chars

    #### debug print ####
    #print(sect_name.decode("utf-8"))
    #print(nbytes2)
    #print(nph) ; print(nrv)
    #print(revDate)
    #print(prHeadI)
    #print(prHeadII)
    #### end of debug print #### 
   
    #######################################################
    #NUMB section
    sect_name = getBinData(file,'char4',1,)[0]       # section name                                #record of 4 char  
    nbnumb = getBinData(file,'int',1,)[0]             # number of bytes in the section              #record of 1 int  
    nn = getBinData(file,'int',1,)[0]                 # nn dimension of nums array                  #record of 1 int    
    nums = []                                    # array of numbers for RATE and ARRAY files   #record of nn int
    for i in range(0,nn):
        nums.append(getBinData(file,'int',1,)[0])

    #### debug print ####
    #print(sect_name)
    #print(nbnumb)
    #print(nn)
    #print(nums)
    #### end of debug print #### 
    
    #######################################################
    #PROP section    
    sect_name = getBinData(file,'char4',1,)[0]       # section name                               #record of 4 char        
    nbprop = getBinData(file,'int',1,)[0]             # number of bytes in prop section            #record of 1 int       
    method = getBinData(file,'int',1,)[0]             # for upward compatibility                   #record of 1 int
    nc = getBinData(file,'int',1,)[0]                 # number of components                       #record of 1 int
    nl = getBinData(file,'int',1,)[0]                 # number of lumped components                #record of 1 int
    nstd = getBinData(file,'int',1,)[0]               # number of standard compositions            #record of 1 int
    ms = getBinData(file,'int',1,)[0]                 # maximum number of standard compositions    #record of 1 int
    mp = getBinData(file,'int',1,)[0]                 # maximum number of phases                   #record of 1 int
   
    
    #records of above dimensions
    PHASNM = getBinData(file,'char16',mp,)     # Names of fluid phases
    COMPNM = getBinData(file,'char16',nc,)     # Names of components
    IDPHAS = getBinData(file,'int',mp,)        # Indicates if phase ip is present (1-oil, 2-gas, 3-water, 4-other)
    IDLOCX = getBinData(file,'int',nc*mp,)     # Indicates if components in phase (0-not, -1 if only component in phase)
    IPCPHZ = getBinData(file,'int',mp,)        # Indicates use of cap press for phase
    AMOLWT = getBinData(file,'float',nc,)       # Molecular weights
    VLIQSC = getBinData(file,'float',nc)       # Molar liquid volume of components
    VGASSC = getBinData(file,'float',nc)       # Molar vapor volume of components
    LUMPNM = getBinData(file,'char16',nl,)     # Names of lumped components
    LUMPCP = getBinData(file,'int',nc*nl,)     # Is component in lumped component
    STDCNM = getBinData(file,'char16',nl,)     # Names of standard compositions
    STDCMP = getBinData(file,'float',nc*ms,)    # Standard compositions
    SURFDENS = getBinData(file,"float",3,)      # Standard compositions    

    #### debug print ####
    #print(sect_name.decode("utf-8"))
    #print(nbprop)
    #print(method, nc, nl, nstd, ms, mp)
    #print()
    #### end of debug print #### 


    #######################################################
    #FLUI section
    sect_name = getBinData(file,'char4',1,)[0]        # section name                        #record of 4 char            
    nbflui = getBinData(file,'int',1,)[0]             # nbflui                              #record of 1 int            
    eos = getBinData(file,'int',1,)[0]                # for black oil eos=0                 #record of 1 int    
    #if(eos == 1):
        # !!!!!!!!!!!!!!!!!   need section to read EoS parameters ()
    
    #### debug print ####
    #print(sect_name.decode("utf-8"))    
    #print(nbflui)
    #print(eos)    
    #print()
    #### end of debug print #### 

    #######################################################
    #LIMI section
    sect_name = getBinData(file,'char4',1,)[0]   # section name                       #record of 4 char      
    nblimi = getBinData(file,'int',1,)[0]        # nblimi                             #record of 1 int
    nlim = getBinData(file,'int',1,)[0]          #nlim                                #record of 1 int
    mstrp = getBinData(file,'int',1,)[0]         #max streams + 1                     #record of 1 int
    mlim = getBinData(file,'int',1,)[0]          #max limits                          #record of 1 int
    method = getBinData(file,'int',1,)[0]        #XXX for upwards compatibility       #record of 1 int   
    print(f"sect_name, nblimi, nlim, mstrp, mlim, method")
    print(f"{sect_name}, {nblimi}, {nlim}, {mstrp}, {mlim}, {method}")
    #records of above dimensions    
    WLIMIT = getBinData(file,'char16',mlim) # Names of well limits
    IDXVAR = getBinData(file,'int',mlim)  # A value of 6 indicates a rate limit, a value <6 indicates a ration limit
    IDSIGN = getBinData(file,'int',mlim)  # Sign associated with the limit
    WLIMITW = getBinData(file,'float',mstrp*mlim) # Well limits weights
    
    #### debug print ####
    #print(sect_name.decode("utf-8"))
    #print(nblimi)
    #print(nlim, mstrp, mlim, method)
    #print()
    #### end of debug print #### 

    #######################################################
    #SEPA section
    sect_name = getBinData(file,'char4',1,)[0]      # section name                        #record of 4 char    
    nbsepa = getBinData(file,'int',1,)[0]          # nbsepa                              #record of 1 int

    XXX = getBinData(file,'int',1,)[0]     # method (for upward compatibility)
    nsep = getBinData(file,'int',1,)[0]    # number of separator specifications
    nistr = getBinData(file,'int',1,)[0]   # number injection streams
    npstr = getBinData(file,'int',1,)[0]   # number production streams
    mstr = getBinData(file,'int',1,)[0]    # maximum streams
    msep = getBinData(file,'int',1,)[0]    # maximum separators
    mcomp = getBinData(file,'int',1,)[0]   # maximum components
    
    #records of above dimensions  
    WSEPNM  = getBinData(file,'char16',msep,)         # Separator names
    WPFLNM  = getBinData(file,'char16',mstr,)         # Production streams
    WIFLNM  = getBinData(file,'char',mstr,)         # Injection streams
    IPSTRM  = getBinData(file,'int',mstr,)          # Is stream oil or gas? (1-Oil, 2-Gas)
    NSPLST  = getBinData(file,'int',msep,)          # Index of last sep in description
    IEKVAR  = getBinData(file,'int',msep,)          # 0: Use fixed K-values; 1: Use EoS
    IEOSDN  = getBinData(file,'int',msep,)          # 0: Fixed density; 1: EoS density
    ISTEMP  = getBinData(file,'int',msep,)          # Temperature index for sep
    IPHSTM  = getBinData(file,'int',mstr,)          # Phase split indicator
    SPTEMP  = getBinData(file,'float',msep,)        # Separator temperature
    SPRESS  = getBinData(file,'float',msep,)        # Separator pressure
    VFSEPR  = getBinData(file,'float',msep,)        # Vapour fraction
    FISTRM  = getBinData(file,'float',mcomp*mstr,)  # Fraction of component in inj stream
    FPSTRM  = getBinData(file,'float',mcomp*mstr,)  # Fraction of component in prod stream
    ZFSEPR  = getBinData(file,'float',2*msep,)      # Liquid and vapour Z-factors
    EKSEPR  = getBinData(file,'float',mcomp*msep,)  # Kvalues for separators
      
    #### debug print ####
    #print(sect_name.decode("utf-8"))    
    #print(nbsepa)
    #print()
    #### end of debug print #### 

    #######################################################
    #RESTART section    
    sect_name = getBinData(file,'char4',1,)[0]        # section name                        #record of 4 char    
    nbrest = getBinData(file,'int',1,)[0]   # nbrest
    niblock = getBinData(file,'int',1,)[0]  # niblock
    
    nrest= getBinData(file,'int',1,)[0]     # number of restarts
    ncpr = getBinData(file,'int',1,)[0]     # number of characters/restart
    nipr = getBinData(file,'int',1,)[0]     # number of integers/restart
    nfpr = getBinData(file,'int',1,)[0]     # number of floats/restart
           
    NAMEOFRUN = ""
    RESTSTEP = []
    STARTTIME = []
    for i in range (0,nrest):
        NAMEOFRUN = getBinData(file,'char16',ncpr,)
        RESTSTEP = getBinData(file,'int',nipr,)
        STARTTIME =getBinData(file,'float',nfpr,)
    #### debug print ####
    print(f"sect_name={sect_name}, nbrest = {nbrest}, niblock = {niblock}")
    print("number of restarts: ",nrest)
    print(ncpr, nipr, nfpr)
    print(NAMEOFRUN)
    print(RESTSTEP)
    print(STARTTIME)
    #### end of debug print #### 
   
    return (SDAT, nums) # returns STARTDATE and NUMS array 


