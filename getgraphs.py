import constants as cts
from datetime import datetime, timedelta

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.dates as md
import matplotlib.pyplot as plt


def make_graph(well_name, x_values, ys_values):
    host = host_subplot(111, axes_class=AA.Axes)
    #plt.subplots(figsize=(20,10))
    plt.subplots_adjust(right=1.0)

    par1 = host.twinx()
    par2 = host.twinx()

    offset = 50

    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",axes=par2, offset=(offset,0))

    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)

    # TODO make function to calculate limits (check defaults, than calculate custom)
    host.get_xaxis().set_major_locator(md.YearLocator())
    host.get_xaxis().set_major_formatter(md.DateFormatter("%d.%m.%Y"))
    host.set_ylim(0,1000)
    par1.set_ylim(0,1000)
    par2.set_ylim(0,100)

    plt.title(f"{well_name}")
    host.set_xlabel("Date")
    host.set_ylabel("P, barsa")
    par1.set_ylabel("Q, sm3/day")
    par2.set_ylabel("WCT, %")


    host.plot(x_values, ys_values[0], '-', color='black', label="WBHP") # BHP
    host.plot(x_values, ys_values[1], '.', markersize=4, color='red', label="WBHPH") # BHPH

    par1.plot(x_values, ys_values[2], '-', color='lime', label="WLPR") # LIQ
    par1.plot(x_values, ys_values[3], '.', markersize=4, color='green', label="WLPRH") # LIQH

    par2.plot(x_values, ys_values[4], '-', color='cyan', label="WWCT") # WCUT
    par2.plot(x_values, ys_values[5], '.', markersize=4, color='cyan', label="WWCTH") # WCUTH

    par1.plot_date(x_values, ys_values[6], '-', color='blue', label="WWIN") # WINJ
    par1.plot_date(x_values, ys_values[7], '.', markersize=4, marker='s', color='blue', label="WWINH") # WINJH
    # TODO find out how to obtain wPI4 values

    # TODO find out how to show a legend
    host.legend(bbox_to_anchor=(0.0, -0.4, 1.0, 0.3), ncol=4, mode="expand", columnspacing=1.0)

    #plt.show()
    plt.savefig(well_name+'_graph.png', bbox_inches='tight')



def get_graphs(currDir, rootName, start_date_array, times, numsArray, RateOut):
    T = len(times)
    MZ = numsArray[5-1]                 # number of connections
    V = cts.VEC + MZ*2*numsArray[55-1]  # number of vectors
    s_d = datetime(start_date_array[2], start_date_array[1], start_date_array[0])

    x_values = [s_d+timedelta(days=x.tos) for x in times]
    y_values = [[],[],[],[],[],[],[],[]]
    
    for well_name in RateOut[1]:
        wi = RateOut[1].index(well_name) 
        for vec in y_values: del vec[:]
        for i in range(T):
            sim_liq =  RateOut[0][T*V*wi+T*cts.Sopr+i]+RateOut[0][T*V*wi+T*cts.Swpr+i]
            hist_liq = RateOut[0][T*V*wi+T*cts.Hopr+i]+RateOut[0][T*V*wi+T*cts.Hwpr+i]

            sim_wcut = 0
            if  RateOut[0][T*V*wi+T*cts.Sopr+i]==0 and RateOut[0][T*V*wi+T*cts.Swpr+i]== 0: sim_wcut = 0
            else: sim_wcut =  RateOut[0][T*V*wi+T*cts.Swpr+i]/sim_liq*100

            hist_wcut = 0
            if  RateOut[0][T*V*wi+T*cts.Hopr+i]==0 and RateOut[0][T*V*wi+T*cts.Hwpr+i]== 0: hist_wcut = 0
            else: sim_wcut =  RateOut[0][T*V*wi+T*cts.Swpr+i]/sim_liq*100


            y_values[0].append(RateOut[0][T*V*wi+T*cts.Sbhp+i]) # simulated BHP
            y_values[1].append(RateOut[0][T*V*wi+T*cts.Hbhp+i]) # history BHP

            y_values[2].append(sim_liq) # simulated Liquid production
            y_values[3].append(hist_liq) # history Liquid production

            y_values[4].append(sim_wcut) # simulated WCUT
            y_values[5].append(hist_wcut) # history WCUT 

            y_values[6].append(RateOut[0][T*V*wi+T*cts.Swir+i]) # simulated Water injection
            y_values[7].append(RateOut[0][T*V*wi+T*cts.Hwir+i]) # history Water injection 

        make_graph(well_name.strip(), x_values, y_values)
        
        '''
        print("---------------------------------")
        print(well_name)
        for i in range(T):
            print(x_values[i], y1_values[i], y2_values[i])
            '''
