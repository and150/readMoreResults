#-*- coding:utf-8 -*-
import constants as cts
import datetime
import time
from dateutil.relativedelta import relativedelta
from datescompare import date2days
from printrate import printRate


def printCptByDate(ResArr, times, T, V,  curr_well_name, curr_well_index,  cptDate, tstep_i, outFile, search_last_bhp=False, search_last_prod=False):

    def get_last_defined_bhp(ResArr, T, V, curr_well_index, tstep_i):
        search_tstep_i = tstep_i
        while search_tstep_i > 0:
            if ResArr[T*V*curr_well_index + T*cts.i_d['Hbhp'] + search_tstep_i] > cts.PTOL:
                return [ResArr[T*V*curr_well_index + T*cts.i_d['Sbhp'] + search_tstep_i], 
                        ResArr[T*V*curr_well_index + T*cts.i_d['Hbhp'] + search_tstep_i], 
                        search_tstep_i]
            search_tstep_i -= 1

        # if something wrong... just return original timestep values
        return [ResArr[T*V*curr_well_index + T*cts.i_d['Sbhp'] + tstep_i], 
                ResArr[T*V*curr_well_index + T*cts.i_d['Hbhp'] + tstep_i], 
                tstep_i]


    def get_last_prod_month(ResArr, T, V, curr_well_index, tstep_i):
        start_wut = ResArr[T*V*curr_well_index + T*cts.i_d['wut'] + tstep_i]

        search_tstep_i = tstep_i
        while search_tstep_i > 0:
            if start_wut - ResArr[T*V*curr_well_index + T*cts.i_d['wut'] + search_tstep_i] >= 30:
                return ( ResArr[T*V*curr_well_index + T*cts.i_d['Sopt'] + search_tstep_i],
                         ResArr[T*V*curr_well_index + T*cts.i_d['Hopt'] + search_tstep_i],
                         ResArr[T*V*curr_well_index + T*cts.i_d['Swpt'] + search_tstep_i],
                         ResArr[T*V*curr_well_index + T*cts.i_d['Hwpt'] + search_tstep_i])
            search_tstep_i -= 1

        # if something wrong
        return (-999.0, -999.0, -999.0, -999.0) 



    outFile.write('{0:s} {1:5.2f} '.format(cptDate, times[tstep_i].tos))  # date and time
    outFile.write('{0:s} '.format(curr_well_name) ) # well name
    
    if search_last_prod:
        latest_prod = get_last_prod_month(ResArr, T, V, curr_well_index, tstep_i)
        outFile.write('{0:5.3f} '.format(latest_prod[0]) )  # simulated cumulative oil
        outFile.write('{0:5.3f} '.format(latest_prod[1]) )  # historic cumulative oil
        outFile.write('{0:5.3f} '.format(latest_prod[2]) )  # simulated cumulative water
        outFile.write('{0:5.3f} '.format(latest_prod[3]) )  # historic cumulative water

    else:
        outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['Sopt'] + tstep_i]) )  # simulated cumulative oil
        outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['Hopt'] + tstep_i]) )  # historic cumulative oil
        
        outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['Swpt'] + tstep_i]) )  # simulated cumulative water
        outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['Hwpt'] + tstep_i]) )  # historic cumulative water


    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['Swit'] + tstep_i]) )  # simulated cumulative injection
    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['Hwit'] + tstep_i]) )  # historic cumulative injection


    # find the latest defined BHP if not defined on the CPT date
    if search_last_bhp:
        latest_defined_pressures = get_last_defined_bhp(ResArr, T, V, curr_well_index, tstep_i)        
        outFile.write('{0:5.3f} '.format(latest_defined_pressures[0]) )  # simulated BHP
        outFile.write('{0:5.3f} '.format(latest_defined_pressures[1]) )  # historic BHP
        #outFile.write(f'{times[latest_defined_pressures[2]].tos} ' )  # debug output of the last defined BHP

        # print THP (TO DO find latest_defined TH pressure)
        outFile.write(f"{ResArr[T*V*curr_well_index + T*cts.i_d['Sthp'] + tstep_i]:5.3f} ")  # simulated THP
        outFile.write(f"{ResArr[T*V*curr_well_index + T*cts.i_d['Hthp'] + tstep_i]:5.3f} ")  # historic THP

    # print BHP on the CPT date (might be undefined if a gauge has been removed) 
    else:
        outFile.write("{0:5.3f} ".format(ResArr[T*V*curr_well_index + T*cts.i_d['Sbhp'] + tstep_i]) )  # simulated BHP
        outFile.write("{0:5.3f} ".format(ResArr[T*V*curr_well_index + T*cts.i_d['Hbhp'] + tstep_i]) )  # historic BHP

        # print THP
        outFile.write(f"{ResArr[T*V*curr_well_index + T*cts.i_d['Sthp'] + tstep_i]:5.3f} ")  # simulated THP
        outFile.write(f"{ResArr[T*V*curr_well_index + T*cts.i_d['Hthp'] + tstep_i]:5.3f} ")  # historic THP


    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.i_d['wut'] + tstep_i]) )  # simulated Uptime 


# function gets date-time and returns timestep number or -1 if date-time not found
def getTimeStepNumber(times, startDate, stringDate="01.01.1900 00:00:00"):
    T = len(times)
    i = T - 1
    CptTime = date2days(stringDate, startDate)
    passedCptDate = False

    while(i>=0):
        if(CptTime >= times[i].tos): 
            passedCptDate = True

        if(abs(CptTime - times[i].tos) < cts.TIMETOL):
            return i
        elif(passedCptDate == True):
            if(abs(CptTime - times[i].tos) <= abs(CptTime - times[i-1].tos)):
                return i
            elif(i>0):
                return i - 1
        i = i - 1
    return -1


# function prints information for cross-plots
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# there is a CONSTANT filter for well names (prints only wells starting with 'WQ2-' and 'WQ-11' and 'WQ-13'
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def getCPT(currDir, rootName, startDate, times, numsArray, RateOut, cptDate):
    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    cptOutFile = open(currDir+"\\"+rootName+".CPT_out","w")
    T = len(times)  
    W = len(wellNames) 
    MZ = numsArray[5-1] 
    V = cts.VEC + MZ*2*numsArray[55-1]       


    # get date one (or more) month behind, number of months set in constants
    cptDate_month_behind = datetime.datetime.strptime(cptDate, "%d.%m.%Y %H:%M:%S")
    cptDate_month_behind = cptDate_month_behind - relativedelta(months = 1)
    cptDate_month_behind = cptDate_month_behind.strftime("%d.%m.%Y %H:%M:%S")
    #print(cptDate, cptDate1)

    # get timestep number for crossplot date and previous date
    tstep_i = getTimeStepNumber(times, startDate, cptDate)
    tstep_j = getTimeStepNumber(times, startDate, cptDate_month_behind)
    #print(tstep_i, tstep_j)


    if(tstep_i>=0 and tstep_j>=0):
        for curr_well_name in wellNames:
            curr_well_index = (wellNames.index(curr_well_name))
            if curr_well_name[0:4] == "WQ2-" or curr_well_name in ["WQ-11", "WQ-13"]: # !!! WQ filter !!!
            #if True:
                printCptByDate(ResArr, times, T, V, curr_well_name, curr_well_index, cptDate,              tstep_i, cptOutFile, False, False)
                printCptByDate(ResArr, times, T, V, curr_well_name, curr_well_index, cptDate_month_behind, tstep_j, cptOutFile, False, True)
                cptOutFile.write('\n')
                #print()
    else:
        print("{0:s} - no such date".format(cptDate))


    cptOutFile.close()
