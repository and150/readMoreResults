from datetime import  date, datetime, timedelta
from operator import itemgetter

def get_zones(layers, indexes):
    if indexes == []:
        return [0 for x in range(len(layers))]

    ii = [0,1]
    idx = indexes[:]
    tf_zones = []
    for x in layers:
        if x > idx[0]:
            idx.append(idx.pop(0))
            ii.append(ii.pop(0))
        tf_zones.append(ii[0])
    return tf_zones


def get_ijk_values_from_array(arrays_dict, dimensions, well_date, connections, out_file, plt_zone_bottom_indexes):

    #print(plt_zone_bottom_indexes)
    #print(  [ x[2] for x in sorted(connections, key=itemgetter(2)) ]  )

    sorted_connections = sorted(connections, key=lambda x:x[2]) 
    zones = get_zones([x[2] for x in sorted_connections], [int(x) for x in plt_zone_bottom_indexes])

    #print(layers, 'aaa')
    #print(get_zones(layers, [int(x) for x in plt_zone_bottom_indexes]))
    #print(sorted_connections)
    #print(zones)
    #for item in zip(sorted_connections, zones):
    #    print(item)


    for item in zip(sorted_connections, zones):
        I,J,K = dimensions[item[0][3]][0], dimensions[item[0][3]][1], dimensions[item[0][3]][2]
        i,j,k = item[0][0]-1,item[0][1]-1,item[0][2]-1

        if item[0][0] and item[0][1] and item[0][2] > 0:
            out_file.write(f"{well_date[0]} {well_date[1]} {item[0][0]} {item[0][1]} {item[0][2]} ") # print connection i-j-k
            for arr_item in arrays_dict[item[0][3]]: # print arrays values
                out_file.write(f"{arrays_dict[item[0][3]][arr_item][I*J*k + I*j + i]} ")
            out_file.write(f"{item[1]}") # zone
            out_file.write("\n")


    '''
    for item in sorted(connections, key=lambda x: x[2]):
        I,J,K = dimensions[item[3]][0], dimensions[item[3]][1], dimensions[item[3]][2]
        i,j,k = item[0]-1,item[1]-1,item[2]-1
        if item[0] and item[1] and item[2] > 0:
            out_file.write(f"{well_date[0]} {well_date[1]} {item[0]} {item[1]} {item[2]} ")
            for arr_item in arrays_dict[item[3]]:
                out_file.write(f"{arrays_dict[item[3]][arr_item][I*J*k + I*j + i]} ")
            out_file.write("\n")
            '''


def get_wells_cells(out_arrays, wells_dates_filename, well_names, perfs_array, times, start_date_array, out_file, plt_items):  # gets values only for perforated cells (perfs from rate-file)
    s_d = datetime(start_date_array[2], start_date_array[1], start_date_array[0])

    #for item in plt_items: print(f"{item} hello from kh list")
    #print()

    ###### alternative for structured perfs_array
    #''' print wells and dates from the request and compose them with indexes of the wells from the model (well_names list)'''
    #wells_dates_from_file = [[ well_names.index(*list(filter(lambda y: y.strip()==x.split()[0], well_names))), x.split()[0], datetime.strptime(' '.join(x.split()[1:]), "%d.%m.%Y %H:%M:%S")] for x in [line.rstrip('\n') for line in open(wells_dates_filename)]]
    #print(wells_dates_from_file) # [well_model_index, well_name, date] # debug

    #selected_wells_perfs = list([well_date[1], well_date[2], *list(filter(lambda time_perf: well_date[0]==time_perf[1] and well_date[2]==s_d+timedelta(days=times[time_perf[0]]), perfs_array))] for well_date in wells_dates_from_file)
    #for item in selected_wells_perfs: print(item) # debug
    ######


    ''' get requested wells and timesteps indexes, well names and dates (extended query) '''
    wells_dates_from_file = [[ well_names.index(*list(filter(lambda y: y.strip()==x.split()[0], well_names))), 
                                x.split()[0],
                                datetime.strptime(' '.join(x.split()[1:]), "%d.%m.%Y %H:%M:%S"),
                                times.index((datetime.strptime(' '.join(x.split()[1:]), "%d.%m.%Y %H:%M:%S")-s_d).days)] for x in [line.rstrip('\n') for line in open(wells_dates_filename)]]
    #print(wells_dates_from_file) # [well_model_index, well_name, date, timestep_index] # debug

    n_wells = len(well_names)
    n_vec = 4 # i, j, k, lgr indexes
    n_k = out_arrays[1][0][2]
    selected_wells_perfs = list([well_date[1], 
                                 well_date[2], 
                                 [well_date[3], well_date[0],
                                 *list( zip(*[iter(perfs_array[ n_wells*n_vec*n_k*well_date[3] + n_vec*n_k*well_date[0] :  n_wells*n_vec*n_k*well_date[3] + n_vec*n_k*well_date[0] +n_vec*n_k])]*n_k) )]] 
                                 for well_date in wells_dates_from_file)
    #for item in selected_wells_perfs: print(item) # debug


    ''' print connection values'''
    for perf_item in selected_wells_perfs:

        plt_zone_bottom_indexes=[]
        if plt_items!=[]:  
            plt_zone_bottom_indexes = sorted([ [abs(x[3]-perf_item[1])]+x for x in plt_items if x[0]==perf_item[0]],key=itemgetter(0))[0][3] 

        get_ijk_values_from_array(out_arrays[0], out_arrays[1], perf_item[0:2], list(zip(perf_item[2][2], perf_item[2][3], perf_item[2][4], perf_item[2][5])), out_file, plt_zone_bottom_indexes)
