#-*- coding:utf-8 -*-
import constants as cts
import datetime
import time
from dateutil.relativedelta import relativedelta
from datescompare import date2days
from printrate import printRate


def printCptByDate(ResArr, times, T, V,  curr_well_name, curr_well_index,  cptDate, tstep_i, outFile, search_last_bhp = False):

    outFile.write('{0:s} {1:5.2f} '.format(cptDate, times[tstep_i].tos))  # date and time
    outFile.write('{0:s} '.format(curr_well_name) ) # well name
    
    outFile.write('{0:3f} '.format(ResArr[T*V*curr_well_index + T*cts.Sopt + tstep_i]) )  # simulated cumulative oil
    outFile.write('{0:3f} '.format(ResArr[T*V*curr_well_index + T*cts.Hopt + tstep_i]) )  # historic cumulative oil

    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.Swit + tstep_i]) )  # simulated cumulative injection
    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.Hwit + tstep_i]) )  # historic cumulative injection

    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.Swpt + tstep_i]) )  # simulated cumulative water
    outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.Hwpt + tstep_i]) )  # historic cumulative water



    def get_last_defined_bhp(ResArr, T, V, curr_well_index, tstep_i):
        search_tstep_i = tstep_i
        while search_tstep_i > 0:
            if ResArr[T*V*curr_well_index + T*cts.Hbhp + search_tstep_i] > cts.PTOL:
                return [ResArr[T*V*curr_well_index + T*cts.Sbhp + search_tstep_i], 
                        ResArr[T*V*curr_well_index + T*cts.Hbhp + search_tstep_i], 
                        search_tstep_i]
            search_tstep_i -= 1

        # if something wrong... just return original timestep values
        return [ResArr[T*V*curr_well_index + T*cts.Sbhp + tstep_i], 
                ResArr[T*V*curr_well_index + T*cts.Hbhp + tstep_i], 
                tstep_i]

    # find the latest defined BHP if not defined on the CPT date
    if search_last_bhp:
        latest_defined_pressures = get_last_defined_bhp(ResArr, T, V, curr_well_index, tstep_i)        
        outFile.write('{0:5.3f} '.format(latest_defined_pressures[0]) )  # simulated BHP
        outFile.write('{0:5.3f} '.format(latest_defined_pressures[1]) )  # historic BHP
        #outFile.write(f'{times[latest_defined_pressures[2]].tos} ' )  # debug output of the last defined BHP

    # print BHP on the CPT date (might be undefined if a gauge has been removed) 
    else:
        outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.Sbhp + tstep_i]) )  # simulated BHP
        outFile.write('{0:5.3f} '.format(ResArr[T*V*curr_well_index + T*cts.Hbhp + tstep_i]) )  # historic BHP

        # print THP
        outFile.write(f'{ResArr[T*V*curr_well_index + T*cts.Sthp + tstep_i]:5.3f} ')  # simulated THP
        outFile.write(f'{ResArr[T*V*curr_well_index + T*cts.Hthp + tstep_i]:5.3f} ')  # historic THP

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

    cptOutFile = open(currDir+"\\"+rootName+".CPTout","w")
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
            # WQ filter !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if curr_well_name[0:4] == "WQ2-" or curr_well_name == "WQ-11" or curr_well_name == "WQ-13":
                printCptByDate(ResArr, times, T, V, curr_well_name, curr_well_index, cptDate, tstep_i, cptOutFile, False)
                printCptByDate(ResArr, times, T, V, curr_well_name, curr_well_index, cptDate_month_behind, tstep_j, cptOutFile)
                cptOutFile.write('\n')
                #print()
    else:
        print("{0:s} - no such date".format(cptDate))


    cptOutFile.close()


#   # debug part
#   with open("../testDateList","r") as dateList:
#       for line in dateList:
#           i = getTimeStepNumber(times, startDate, line.strip('\n'))
#           if(i>=0):
#
#               for x in wellNames:
#                   wi = (wellNames.index(x))
#                   ##debug output
#                   #print('{0:s} - timestep={1:4d}  tos = {2:5.11f} '.format(line.strip('\n'), i, times[i].tos),end= ' ' ) 
#
#                   print('{0:s} {1:5.2f} '.format(line.strip('\n'), times[i].tos), end = ' ' ) 
#
#                   print('{0:s}'.format(x), end = ' ') #
#                   
#                   print('{0:3f}'.format(ResArr[T*V*wi + T*cts.Sopt + i]), end = ' ')  #
#                   print('{0:3f}'.format(ResArr[T*V*wi + T*cts.Hopt + i]), end = ' ')  #
#
#                   print(' ',end=' ')
#
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Swit + i]), end = ' ')  # 
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Hwit + i]), end = ' ')  # 
#
#                   print(' ',end=' ')
#
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Swpt + i]), end = ' ')  # 
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Hwpt + i]), end = ' ')  # 
#                   
#                   print(' ',end=' ')
#
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Sbhp + i]), end = ' ')  # 
#                   print('{0:5.3f}'.format(ResArr[T*V*wi + T*cts.Hbhp + i]), end = ' ')  # 
#                   
#                   print()
#
#           else:
#               print("{0:s} - no such date".format(line.strip('\n')))


        

#    dateList.close()





