#-*- coding:utf-8 -*-
import argparse
import sys
import os
import mmap
import cProfile, pstats, io
import numpy as np


from readmisc import readMISC 
from readctl  import readCTL  
from readrate import readRATE 
#from readrt import readRATE 

import getwt
import getit
import getplt
import getcpt
import getStartRate
from printrate import printRate


def readMore(currDir, rootName): # read MORE result files
    # MISC
    with open(currDir+"\\"+rootName+".mis", "r+b") as file: 
	    miscFile = mmap.mmap(file.fileno(),0)
    miscOut = readMISC(miscFile);
    startDate = miscOut[0]
    numsArray = miscOut[1]
    miscFile.close()        

    # CTL
    with open(currDir+"\\"+rootName+".ctl", "r+b") as file:  
	    ctlFile = mmap.mmap(file.fileno(),0)
    times = readCTL(ctlFile); 
    ctlFile.close()                   

    # RATE
    with open(currDir+"\\"+rootName+".rat", "r+b") as file:  
	    RateOut = readRATE(file, numsArray, times) 
    return(startDate, times, numsArray, RateOut)


  
# profiler start
#pr = cProfile.Profile()
#pr.enable()

#currDir = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="provides a name of *.mis file to read")
parser.add_argument("-w","--WT", action="store_true", help ="generates well tests output")
parser.add_argument("-i","--IT", action="store_true", help ="generates well interferention tests output")
parser.add_argument("-p","--PLT", action="store_true", help ="generates production logging tests output")
parser.add_argument("-c","--CPT", action="store", help ="generates crossplots by certain date", default="-999")
parser.add_argument("-a","--AVR", action="store_true", help ="generates start oil rates, average oil rates for the first year of production and cumulatieves")
args = parser.parse_args()

currDir = os.path.dirname( os.path.abspath(args.inputfile))
rootName = os.path.basename(args.inputfile).split('.')[0]

print(currDir, rootName)


try:
    # global variables
    out = []          # results array

    #read MORE results
    out = readMore(currDir,rootName)

    startDate = out[0]
    times = out[1]
    numsArray = out[2]
    RateOut = out[3]

    if args.CPT!="-999":
        # crossplot generation 
        getcpt.getCPT(currDir, rootName, startDate, times, numsArray, RateOut, args.CPT)      

    if args.WT:
        # well test results output
        getwt.getWT(currDir, rootName, startDate, times, numsArray, RateOut)      

    if args.IT:
        # well test results output
        getit.getIT(currDir, rootName, startDate, times, numsArray, RateOut)      
        
    if args.PLT:
        # PLT profiles output 
        getplt.getPLT(currDir, rootName, startDate, times, numsArray, RateOut)

    if args.AVR:
        # start rates, first year av.rates and cumulatives export
        getStartRate.getAVRCUM(currDir, rootName, startDate, times, numsArray, RateOut)

#    else:
#        print("no action chosen for {}".format(rootName))


    #printRate(times, numsArray, RateOut) 
    #print(time.time()-stime)
    # profiler parameters output
    #pr.disable()
    #s = io.StringIO()   
    #ps = pstats.Stats(pr, stream = s)
    #ps.print_stats()
    #print(s.getvalue())

except IOError as Argument:
    print("Error: ", Argument)
