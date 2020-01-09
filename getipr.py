#-*- coding:utf-8 -*-
import constants as cts
from datetime import  datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

def getIPR(currDir, rootName, start_date_array, times, numsArray, RateOut):
    ResArr, well_names = RateOut[0], RateOut[1]
    T = len(times)                      # amount of RATE-file entries
    MZ = numsArray[5-1]                 # number of connections
    V = cts.VEC + MZ*2*numsArray[55-1]  # number of vectors
    s_d = datetime(start_date_array[2], start_date_array[1], start_date_array[0])

    ipr_file_name   = currDir+"\\"+rootName+".IPRlist"        # well IPR times input file name
    out_file  = open(currDir+"\\"+rootName+".IPR_out", "w") # well PI out file

    """read IPR list """
    ipr_dict, ipr_index, date_time = {}, '', 0
    for x in filter(lambda x: len(x)>0, [line.rstrip('\n') for line in open(ipr_file_name)]):
        w = x.split()
        ipr_index = w[0]+'_'+w[3]
        date_time = datetime.strptime(' '.join(w[1:3]), "%d.%m.%Y %H:%M:%S")
        if ipr_index in ipr_dict:
            ipr_dict[ipr_index].append(date_time)
        else:
            ipr_dict.update({ipr_index:[date_time]})
    #for item in ipr_dict: print(item[:-2], item[-1], ipr_dict[item]) # debug

    """ get IPR actual and model pressures and rates from rate file """
    ipr_dict_for_regr = {}
    for ipr_item in ipr_dict:
        wi = ([x.strip() for x in RateOut[1]].index(ipr_item[:-2])) # get well index
        for date_time in ipr_dict[ipr_item]:
            i =[datetime(t.year, t.month, t.day, t.hour, t.minute, t.second) for t in [s_d+timedelta(days=x.tos) for x in times]].index(date_time) # get time index

            Q_sim  = ResArr[T*V*wi+T*cts.i_d['Sopr']+i]+ResArr[T*V*wi+T*cts.i_d['Swpr']+i]+ResArr[T*V*wi+T*cts.i_d['Swir']+i]  # simulated oil + water+injection rate 
            Q_hist = ResArr[T*V*wi+T*cts.i_d['Hopr']+i]+ResArr[T*V*wi+T*cts.i_d['Hwpr']+i]+ResArr[T*V*wi+T*cts.i_d['Hwir']+i]  # historic oil + water+injection rate
            P_sim  = ResArr[T*V*wi+T*cts.i_d['Sbhp']+i]  # simulated BHP
            P_hist = ResArr[T*V*wi+T*cts.i_d['Hbhp']+i]  # historic BHP

            if ipr_item in ipr_dict_for_regr:
                ipr_dict_for_regr[ipr_item][0].append(Q_sim)
                ipr_dict_for_regr[ipr_item][1].append(Q_hist)
                ipr_dict_for_regr[ipr_item][2].append(P_sim)
                ipr_dict_for_regr[ipr_item][3].append(P_hist)
            else:
                ipr_dict_for_regr.update({ipr_item:[[Q_sim],[Q_hist],[P_sim],[P_hist]]})

    """ obtain PI values from IPR data (by linear regression)"""
    out_file.write("Well IPR_number first_date  PI_sim PI_hist BHP_last_sim BHP_last_hist\n")
    model = LinearRegression()
    for item in ipr_dict_for_regr:

        x = np.array(ipr_dict_for_regr[item][2]).reshape((-1,1)) # P_sim
        y = np.array(ipr_dict_for_regr[item][0]) # Q_sim
        model.fit(x,y)
        PI_sim = model.coef_[0]

        x = np.array(ipr_dict_for_regr[item][3]).reshape((-1,1)) # P_hist
        y = np.array(ipr_dict_for_regr[item][1]) # Q_hist
        model.fit(x,y)
        PI_hist = model.coef_[0]

        #print(f"{item[:-2]} {item[-1]} {ipr_dict[item][0]} {PI_sim} {PI_hist} {ipr_dict_for_regr[item][2][-1]} {ipr_dict_for_regr[item][3][-1]}") # well ipr_number first_sample_date  PI_sim PI_hist P_last_sim P_last_hist
        out_file.write(f"{item[:-2]} {item[-1]} {ipr_dict[item][0]} {PI_sim} {PI_hist} {ipr_dict_for_regr[item][2][-1]} {ipr_dict_for_regr[item][3][-1]}\n") # well ipr_number first_sample_date  PI_sim PI_hist P_last_sim P_last_hist

    out_file.close()

