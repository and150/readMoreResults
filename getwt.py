#-*- coding:utf-8 -*-
import constants as cts
from item_class import *
from datescompare import  date2days


def check_not_gap(well, day, start_date, gap_list):

    for gap_item in gap_list:
        if well==gap_item[0] and day >= date2days(gap_item[1], start_date) and day <= date2days(gap_item[2], start_date):
            return False
    return True





# get graphs of pressure for well tests and get statistics for well production indexes
def getWT(currDir, rootName, startDate, times, numsArray, RateOut):

    ResArr = RateOut[0]
    wellNames = RateOut[1]
    for i in range(0,len(wellNames)):
        wellNames[i] = wellNames[i].rstrip()

    wtFileName   = currDir+"\\"+rootName+".WTlist"  # well test list input file name
    outFile  = open(currDir+"\\"+rootName+".WT_graphs", "w") # graphs output
    wtOutFile = open(currDir+"\\"+rootName+".WT_out","w") # parameters output
    wtOutFile.write("WTnumb  well startPBU LIQ  LIQH  BHP  BHPH  Press  PressH stopPBU\n") # header

    gap_list_test = [   
                    ('P1', '09.10.2017 0:00:00', '10.10.2017 1:00:00'), 
                    ('P1', '09.05.2020 0:00:00', '11.06.2020 7:00:00'), 
                    ('P1', '07.10.2021 0:00:00', '10.10.2021 0:00:00') 
                    ]

    gap_list = [
            ('WQ2-129', '04.05.2020 15:59:00', '05.05.2020 09:10:00'),
            ('WQ2-142', '04.05.2020 19:59:00', '05.05.2020 09:10:00'),
            ('WQ2-167', '04.05.2020 19:59:00', '05.05.2020 08:10:00'),
            ('WQ2-333', '04.05.2020 22:00:00', '05.05.2020 06:10:00'),
            ('WQ2-341', '04.05.2020 22:00:00', '05.05.2020 06:10:00'),
            ('WQ2-343', '04.05.2020 22:00:00', '05.05.2020 06:10:00')
            ]

    ####### well test list processing #######
    WTlist = test_items()
    WTlist.get_items_list(wtFileName, startDate)
      
    liqCut = cts.LIQCUT
    PBUstr = ""
    not_gap = True                     # variable for excluding non-zero rate periods from PBU-end check  - переменная для исключения незначащих ненулевых дебитов из проверки конца КВД
    T = len(times)                      # amount of RATE-file entries
    MZ = numsArray[5-1]                 # number of connections
    V = cts.VEC + MZ*2*numsArray[55-1]  # number of vectors

    for x in WTlist.items_list: # for all wells and tests
        PBUstr = ""
        not_gap = True

        wi = (wellNames.index(x.well))     
        for i in range(0,T): # for all times of RATE-file
            # output only within welltest period
            if(times[i].tos >= x.start and times[i].tos <= x.stop):             
                # output to *.WTgraphs  no filters
                outFile.write("\n")
                outFile.write("WT=" + str(x.wt)+ " ")                            # test number
                outStr = str(times[i].tos) +" " + str(wellNames[wi]+" "); outFile.write(outStr) # time and well name

                outFile.write(str(ResArr[T*V*wi + T* cts.i_d['Sbhp'] + i])); outFile.write(" ")  # simulated BHP
                outFile.write(str(ResArr[T*V*wi + T* cts.i_d['Sopr'] + i])); outFile.write(" ")  # simulatdd oil rate
                outFile.write(str(ResArr[T*V*wi + T* cts.i_d['Swpr'] + i] + ResArr[T*V*wi + T* cts.i_d['Swir'] + i])); outFile.write(" ")  # simulated water rate (injection)

                outFile.write(str(ResArr[T*V*wi + T* cts.i_d['Hbhp'] + i])); outFile.write(" ")  # historic BHP
                outFile.write(str(ResArr[T*V*wi + T* cts.i_d['Hopr'] + i])); outFile.write(" ")  # historic oil rate
                outFile.write(str(ResArr[T*V*wi + T* cts.i_d['Hwpr'] + i] + ResArr[T*V*wi + T* cts.i_d['Hwir'] + i])); outFile.write(" ")  # historic water rate + injection
                

                # get PBU and print parameters to *.WTout
                # PBU rates calculation
                currLiq  = ResArr[T*V*wi + T* cts.i_d['Sopr'] + i] + ResArr[T*V*wi + T* cts.i_d['Swpr'] + i] + ResArr[T*V*wi + T* cts.i_d['Swir'] + i]# current simulated liquid rate
                currLiqH = ResArr[T*V*wi + T* cts.i_d['Hopr'] + i] + ResArr[T*V*wi + T* cts.i_d['Hwpr'] + i] + ResArr[T*V*wi + T* cts.i_d['Hwir'] + i]# current historic liquid rate

                currOil  = ResArr[T*V*wi + T* cts.i_d['Sopr'] + i] # current simulated oil rate
                currOilH = ResArr[T*V*wi + T* cts.i_d['Hopr'] + i] # current actual oil rate

                currP  = ResArr[T*V*wi + T* cts.i_d['Sbhp'] + i]   # simulatde BHP
                currPH = ResArr[T*V*wi + T* cts.i_d['Hbhp'] + i]   # historic BHP

                #print(f"{x.well} {times[i].tos:.2f} {currOilH:.2f}")

                maxP = currP
                maxPH = currPH
                if currP <= cts.PTOL or currPH <= cts.PTOL :
                    maxP, maxPH = maxP, maxPH
                else:
                    maxP, maxPH = currP, currPH

                if i<=len(times):  
                    nextLiq = ResArr[T*V*wi + T* cts.i_d['Sopr'] + i+1] + ResArr[T*V*wi + T* cts.i_d['Swpr'] + i+1]+ ResArr[T*V*wi + T* cts.i_d['Swir'] + i+1] # next simulated liquid rate
                else: 
                    nextLiq = currLiq



                # check if entry inside non-zero rate period 
                not_gap = check_not_gap(x.well, times[i].tos, startDate, gap_list) 

    
                if(currLiq > liqCut):   # check intervals with non-zero rate
                    outFile.write(" dynamic") 

                    if nextLiq <= liqCut and not_gap: # print parameters just before PBU (rate and BHP)                           
                        PBUstr = PBUstr + x.well + " " + str(times[i].tos) # name of the well and PBU start time
                        PBUstr = PBUstr + " " + str(currLiq) + " " + str(currLiqH) # simulated and historic rates(injectivities) of liquid
                        ###PBUstr = PBUstr + " " + str(currOil) + " " + str(currOilH) # simulated and historic oil rates
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.i_d['Sbhp'] + i]) # simulated BHP
                        PBUstr = PBUstr + " " + str(ResArr[T*V*wi + T* cts.i_d['Hbhp'] + i])  # historic BHP
                else:
                    outFile.write(" static")                    
                    if nextLiq > liqCut and not_gap: break # stop cycle after the first PBU read
                    #if(nextLiq > liqCut): break # stop cycle after the first PBU read

        PBUstr = PBUstr + " " + str(maxP)   # simulated reservoir pressure
        PBUstr = PBUstr + " " + str(maxPH)   # historic reservoir pressure
        PBUstr = PBUstr + " " + str(times[i].tos)  # PBU stop time

        wtOutFile.write("WT="+str(x.wt)+" "+PBUstr+"\n")  # PBU parameters output

    outFile.close()
    wtOutFile.close()
