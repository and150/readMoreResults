from datetime import  date, datetime, timedelta

def get_ijk_values_from_array(arrays_dict, dimensions, well_date, connections):
    I,J,K = dimensions[0], dimensions[1], dimensions[2]
    #print(f"I,J,K = {I}, {J}, {K}")
    for item in connections:
        #print(f"item perf = {item}")
        i,j,k = item[0]-1,item[1]-1,item[2]-1
        if item[0] and item[1] and item[2] > 0:
            print(well_date[0], well_date[1], item[0],item[1],item[2], end=" ")
            for arr_item in arrays_dict:
                print(arrays_dict[arr_item][I*J*k + I*j + i], end=" ")
            print()



def get_wells_cells(out_arrays, wells_dates_filename, well_names, times_perfs, times, start_date_array):
    s_d = datetime(start_date_array[2], start_date_array[1], start_date_array[0])
    #for item in out_arrays: print(item)

    # print wells and dates from the request and compose them with indexes of the wells from the model (well_names list)
    wells_dates_from_file = [[ well_names.index(*list(filter(lambda y: y.strip()==x.split()[0], well_names))), x.split()[0], datetime.strptime(' '.join(x.split()[1:]), "%d.%m.%Y %H:%M:%S")] for x in [line.rstrip('\n') for line in open(wells_dates_filename)]]
    #print(wells_dates_from_file) # [well_model_index, well_name, date]

    selected_wells_perfs = list( [well_date[1], well_date[2], *list(filter(lambda time_perf: well_date[0]==time_perf[1] and well_date[2]==s_d+timedelta(days=times[time_perf[0]]), times_perfs))] for well_date in wells_dates_from_file)
    #for item in selected_wells_perfs: print(item)



    #TODO find out how to distinguish if a well is in LGR and the number of this LGR if any 
    # print connection values
    for perf_item in selected_wells_perfs:
        get_ijk_values_from_array(out_arrays[0], out_arrays[2][0], perf_item[0:2], list(zip(perf_item[2][2], perf_item[2][3], perf_item[2][4])))







    #dates = [date(start_date[2], start_date[1], start_date[0]) + timedelta(days=x) for x in times]
    #print(dates)

    #print(f"Main_arrays\n{out_arrays[0]}")
    #print(f"LG_arrays\n{out_arrays[1]}")
    #print( [(item) for item in out_arrays[0]]) # debug Main grid arrays printing
    #print( [(item, out_arrays[0][item]) for item in out_arrays[0]]) # debug Main grid arrays printing
    #or lgr in out_arrays[1]: print( [(item, lgr[item]) for item in lgr] ) # debug LG grids arrays printing
    #print(f"grid_dimensions={out_arrays[2]}")


    #print(f"\n wells_dates_filename\n{wells_dates_filename}")
    #print(f"\n well_names\n{well_names}")
    #print(f"\n times_perfs\n{times_perfs}")  #[timestep, well_index, [perf_i], [perf_j], [perf_k]]


    #for item in times_perfs: 
    #  for well_item in wells_dates_from_file:
    #      if well_item[2] ==  s_d+timedelta(days=item[0]):
    #          print('aaaaaa', s_d + timedelta(days=item[0]), item[0], item[1], item[2])

    #print()
    #print(f"times\n{times}")

    #print()
    #print(start_date, date(start_date[2], start_date[1], start_date[0]))

    #for step in times:
    #    print(f"step={step}, {datetime(start_date_array[2], start_date_array[1], start_date_array[0]) + timedelta(days=step)}") 
