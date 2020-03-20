#-*- coding:utf-8 -*-
import constants as cts
from item_class import *
from datetime import datetime

'''
class plt_item(test_item):
    def __init__(self, *args):
        self.args = args

        self.well = args[0]     # well name
        self.start = args[1]    # test start time
        self.plt_ints = args[2] # array of plt intervals 

class plt_items(test_items):
    def get_items_list(self, filename, SDAT):
        lines = [line.rstrip('\n') for line in open(filename)]
        for x in lines:
            if len(x) > 0:
                words = x.split()
                self.items_list.append(plt_item( words[0],
                    date2days(words[1] + " " + words[2], SDAT),
                    words[3:] ))
                    '''

'''
def printPlt(pltItem, pltarr, pltLR, times, wellNames, tstep, wnumb, pltOutFile):
    pltOutFile.write( '{} {} '.format( times[tstep].tos, wellNames[wnumb]) ) 
    s = 0
    f = s
    for i in range(0, len(pltItem.plt_ints)):
        f = int(pltItem.plt_ints[i])
        pltOutFile.write( '{:.3f} '.format(sum(pltarr[s:f])/pltLR ))                    
        s = f
    pltOutFile.write('\n')
    '''

def print_plt(pltItem, pltarr, pltLR, times, wellNames, tstep, wnumb, pltOutFile):
    pltOutFile.write( '{} {} '.format( times[tstep].tos, wellNames[wnumb]) ) 
    s = 0
    f = s
    #for i in range(0, len(pltItem.plt_ints)):
    for i in range(0, len(pltItem[2])):
        f = int(pltItem[2][i])
        pltOutFile.write( '{:.3f} '.format(sum(pltarr[s:f])/pltLR ))                    
        s = f
    pltOutFile.write('\n')


def plt_items_from_file(file_name, start_date):
    with open(file_name, 'r') as input_file:
        return [ [x[0], date2days(x[1]+" "+x[2],start_date), x[3:], datetime.strptime(x[1]+" "+x[2], "%d.%m.%Y %H:%M:%S")] for x in [line.split() for line in input_file if len(line)>0]] 


def getPLT(currDir, rootName, startDate, times, numsArray, RateOut):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    pltFileName = currDir+"\\"+rootName+".PLTlist"  # input PLT list
    pltOutFile = open(currDir+"\\"+rootName+".PLT_out","w") # PLT out file

    MZ = numsArray[5-1]                 # number of layers
    T = len(times)                      # rate file records number
    #W = len(wellNames) # wells amount
    V = cts.VEC + MZ*2*numsArray[55-1]  # vectors amount 
    Vbase = cts.VEC

    '''
    PLTlist = plt_items()
    PLTlist.get_items_list(pltFileName, startDate)
    for x in PLTlist.items_list: # for all wells and PLTs
        #print("___", x.well, x.start, x.plt_ints) # debug

        j = (wellNames.index(x.well))     
        for i in range(0,len(times)):
            if(abs(times[i].tos - x.start) <= cts.TIMETOL+ 0.001): 
                pltarr = [0]*MZ 
                for k in range(0,MZ):
                    # temporaty PLT-vector for every timestep for every well                   
                    pltarr[k] = ResArr[T*V*j + T*(Vbase+k) + i] + ResArr[T*V*j + T*(Vbase+MZ+k) + i] 

                pltLR = sum(pltarr) 
                if pltLR != 0: 
                    printPlt(x, pltarr, pltLR, times, wellNames, i , j, pltOutFile)
                else:
                	pltOutFile.write( '{} {}  liquid_rate=0\n'.format( times[i].tos, wellNames[j] ) )                                    
                        '''
    plt_items = plt_items_from_file(pltFileName, startDate)
    for item in plt_items: # for all wells and PLTs
        j = (wellNames.index(item[0]))     
        for i in range(0,len(times)):
            if(abs(times[i].tos - item[1]) <= cts.TIMETOL+ 0.001): 
                pltarr = [0]*MZ 
                for k in range(0,MZ):
                    pltarr[k] = ResArr[T*V*j + T*(Vbase+k) + i] + ResArr[T*V*j + T*(Vbase+MZ+k) + i] # temporary PLT-vector for every timestep for every
                pltLR = sum(pltarr) 
                if pltLR != 0: 
                    print_plt(item, pltarr, pltLR, times, wellNames, i , j, pltOutFile)
                else:
                    pltOutFile.write( '{} {}  liquid_rate=0\n'.format( times[i].tos, wellNames[j] ) )                                    
    return plt_items
