import constants as cts
import statistics
from datetime import datetime, timedelta
from pathlib import Path

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.dates as md
import matplotlib.pyplot as plt


def make_graph(root_name, well_name, x_values, ys_values):
    host = host_subplot(111, axes_class=AA.Axes)
    #plt.subplots(figsize=(20,10))
    plt.subplots_adjust(right=1.0)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",axes=par2, offset=(50,0))

    new_fixed_axis = par3.get_grid_helper().new_fixed_axis
    par3.axis["right"] = new_fixed_axis(loc="right",axes=par3, offset=(100,0))

    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)
    par3.axis["right"].toggle(all=True)

    host.get_xaxis().set_major_locator(md.YearLocator())
    host.get_xaxis().set_major_formatter(md.DateFormatter("%d.%m.%Y"))

    # TODO make function to calculate limits (check defaults, than calculate custom)
    pres_lim = max(max(ys_values['Sbhp']), max(ys_values['Hbhp']))
    liq_lim = max(max(ys_values['Sliq']), max(ys_values['Hliq']), max(ys_values['Swir']), max(ys_values['Hwir']))

    wPI_lim = max(ys_values['wPI4']) 
    if wPI_lim > 10000: wPI_lim = statistics.median(ys_values['wPI4']) + 1000 

    host.set_xlim(x_values[next((x for x,y in enumerate(ys_values['Hliq']) if y) ,0)], x_values[-1]) # set datetime limits
    host.set_ylim(0,pres_lim) # pressure
    par1.set_ylim(0,liq_lim) # liquid and injection
    par2.set_ylim(0,100) # wcut
    par3.set_ylim(0,wPI_lim) # wPI

    plt.title(f"{well_name}")
    host.set_xlabel("Date")
    host.set_ylabel("P, barsa")
    par1.set_ylabel("Q, sm3/day")
    par2.set_ylabel("WCT, %")
    par3.set_ylabel("WPI")

    host.plot(x_values, ys_values['Sbhp'], '-', color='black', label="WBHP", linewidth=0.8, zorder=10) # BHP
    host.plot(x_values, ys_values['Hbhp'], '.', markersize=4, color='red', label="WBHPH", zorder=0) # BHPH

    par1.plot(x_values, ys_values['Sliq'], '-', color='lime', label="WLPR", linewidth=0.8, zorder=10) # LIQ
    par1.plot(x_values, ys_values['Hliq'], '.', markersize=3, color='green', label="WLPRH", zorder=0) # LIQH

    par2.plot(x_values, ys_values['Swcut'], '-', color='cyan', label="WWCT", linewidth=0.8, zorder=10) # WCUT
    par2.plot(x_values, ys_values['Hwcut'], '.', markersize=3, color='cyan', label="WWCTH", zorder=0) # WCUTH

    par1.plot_date(x_values, ys_values['Swir'], '-', color='blue', label="WWIN", linewidth=0.8, zorder=10) # WINJ
    par1.plot_date(x_values, ys_values['Hwir'], '.', markersize=2, marker='s', color='blue', label="WWINH", zorder=0) # WINJH

    par3.plot(x_values, ys_values['wPI4'], '-', color='magenta', label="wPI4", linewidth=0.5, zorder=5) # wPI4

    host.legend(bbox_to_anchor=(0.0, -0.4, 1.0, 0.3), ncol=5, mode="expand", columnspacing=1.0) # dimensions hardcoded :(

    # TODO find out how to add table with statistics at the bottom of the picture
    rows = [well_name]
    columns = ('header1', 'header2', 'header3', 'header4', 'header5')
    cell_text = [[111, 222, 333, 444, 555]]
    plt.table(cellText=cell_text, rowLabels=rows, colLabels=columns, bbox=(-0.10, -0.42, 1.35, 0.10)) # dimensions hardcoded :(

    # TODO save pictures into pptx file
    plt.savefig('./'+root_name+'_pics/'+well_name+'_graph.png', dpi=600, bbox_inches='tight') # plt.show()
    plt.close()



def get_graphs(currDir, rootName, start_date_array, times, numsArray, RateOut):

    Path(rootName+"_pics").mkdir(parents=True, exist_ok=True)

    T = len(times)
    MZ = numsArray[5-1]                 # number of connections
    V = cts.VEC + MZ*2*numsArray[55-1]  # number of vectors
    s_d = datetime(start_date_array[2], start_date_array[1], start_date_array[0])

    x_values = [s_d+timedelta(days=x.tos) for x in times]
    y_values = {} 

    for well_name in RateOut[1]: # no filters
    #for well_name in list(filter(lambda x: 'WQ2-' in x or 'WQ-11' in x or 'WQ-13' in x, RateOut[1])): # WQ filter
        wi = RateOut[1].index(well_name) 
        y_values.clear()
        y_values = {'Sbhp':[], 'Hbhp':[], 'Sliq':[], 'Hliq':[], 'Swcut':[], 'Hwcut':[], 'Swir':[], 'Hwir':[], 'wPI4':[]}
        for i in range(T):
            sim_liq =  RateOut[0][T*V*wi+T*cts.i_d['Sopr']+i]+RateOut[0][T*V*wi+T*cts.i_d['Swpr']+i]
            hist_liq = RateOut[0][T*V*wi+T*cts.i_d['Hopr']+i]+RateOut[0][T*V*wi+T*cts.i_d['Hwpr']+i]

            sim_wcut = 0
            if  RateOut[0][T*V*wi+T*cts.i_d['Sopr']+i]==0 and RateOut[0][T*V*wi+T*cts.i_d['Swpr']+i]== 0: sim_wcut = 0
            else: sim_wcut =  RateOut[0][T*V*wi+T*cts.i_d['Swpr']+i]/sim_liq*100

            hist_wcut = 0
            if  RateOut[0][T*V*wi+T*cts.i_d['Hopr']+i]==0 and RateOut[0][T*V*wi+T*cts.i_d['Hwpr']+i]== 0: hist_wcut = 0
            else: hist_wcut =  RateOut[0][T*V*wi+T*cts.i_d['Hwpr']+i]/sim_liq*100

            y_values['Sbhp'].append(RateOut[0][T*V*wi+T*cts.i_d['Sbhp']+i]) # simulated BHP
            y_values['Hbhp'].append(RateOut[0][T*V*wi+T*cts.i_d['Hbhp']+i]) # history BHP
            y_values['Sliq'].append(sim_liq) # simulated Liquid production
            y_values['Hliq'].append(hist_liq) # history Liquid production
            y_values['Swcut'].append(sim_wcut) # simulated WCUT
            y_values['Hwcut'].append(hist_wcut) # history WCUT 
            y_values['Swir'].append(RateOut[0][T*V*wi+T*cts.i_d['Swir']+i]) # simulated Water injection
            y_values['Hwir'].append(RateOut[0][T*V*wi+T*cts.i_d['Hwir']+i]) # history Water injection 
            y_values['wPI4'].append(RateOut[0][T*V*wi+T*cts.i_d['wPI4']+i]) # simulated well production index 4-point 

        make_graph(rootName, well_name.strip(), x_values, y_values)
