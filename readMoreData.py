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
from readgrd  import read_static_arrays
#from readrt import readRATE 

import getkh
import getwt
import getipr
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

def read_grd(currDir, rootName, out_arrays_names): # read MORE Grid file
    # GRID
    with open(currDir+"\\"+rootName+".grd", "r+b") as file:  
        return read_static_arrays(file,out_arrays_names) 
    #return(grd_out)


  
# profiler start
#pr = cProfile.Profile()
#pr.enable()

#currDir = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="provides a name of *.mis file to read")
parser.add_argument("-w","--WT", action="store_true", help ="generates well tests output")
parser.add_argument("-i","--IT", action="store_true", help ="generates well interferention tests output")
parser.add_argument("-r","--IPR", action="store_true", help ="generates IPR tests output")
parser.add_argument("-p","--PLT", action="store_true", help ="generates production logging tests output")
parser.add_argument("-c","--CPT", action="store", help ="generates crossplots by certain date", default="-999")
parser.add_argument("-k","--KH", action="store", help ="get perms and h-s from static array file")
parser.add_argument("-a","--AVR", action="store_true", help ="generates start oil rates, average oil rates for the first year of production and cumulatieves")
args = parser.parse_args()

currDir = os.path.dirname( os.path.abspath(args.inputfile))
rootName = os.path.basename(args.inputfile).split('.')[0]
#print(currDir, rootName)

try:
    """read MORE results """
    out = readMore(currDir,rootName) # results array
    startDate, times, numsArray, RateOut = out[0], out[1], out[2], out[3]
    well_names, perfs_array = RateOut[1], RateOut[2]

    """ crossplot generation """
    if args.CPT!="-999": 
        getcpt.getCPT(currDir, rootName, startDate, times, numsArray, RateOut, args.CPT)      

    """ well test results output (PI) """
    if args.WT:
        getwt.getWT(currDir, rootName, startDate, times, numsArray, RateOut)      

    """ well test results output """
    if args.IT:
        getit.getIT(currDir, rootName, startDate, times, numsArray, RateOut)      
        
    """ well IPR results output (PI) """
    if args.IPR:
        getipr.getIPR(currDir, rootName, startDate, times, numsArray, RateOut)      

    """ PLT profiles output """
    if args.PLT:
        getplt.getPLT(currDir, rootName, startDate, times, numsArray, RateOut)

    """ GRID read """
    if args.KH:
        out_arrays_names = ['DZTV','PERMX', 'PERMY'] #['DZTV','PERMX','PERMY'] 
        out_arrays = read_grd(currDir,rootName, out_arrays_names) # reads some static arrays
        with open(currDir+"\\"+rootName+".kh_out","w") as kh_out_file:
            getkh.get_wells_cells(out_arrays, args.KH, well_names, perfs_array, [x.tos for x in times], startDate, kh_out_file)


    """ start rates, first year av.rates and cumulatives export """
    if args.AVR:
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
