from datetime import  date, datetime, timedelta

def get_wells_cells(out_arrays, wells_dates_filename, well_names, perfs_array, times, start_date):

    wells_dates_from_file = [[x.split()[0], datetime.strptime(' '.join(x.split()[1:]), "%d.%m.%Y %H:%M:%S")] for x in [line.rstrip('\n') for line in open(wells_dates_filename)]]
    #print(wells_dates_from_file)

    dates = [date(start_date[2], start_date[1], start_date[0]) + timedelta(days=x) for x in times]
    #print(dates)


    #print(f"Main_arrays\n{out_arrays[0]}")
    #print(f"LG_arrays\n{out_arrays[1]}")
    #print( [(item, out_arrays[0][item]) for item in out_arrays[0]]) # debug Main grid arrays printing
    #or lgr in out_arrays[1]: print( [(item, lgr[item]) for item in lgr] ) # debug LG grids arrays printing
    #print(f"grid_dimensions={out_arrays[2]}")


    #TODO pass here GRID and LGRs dimensions
    #TODO choose dates_from_file form dates
    #TODO find out how to distinguish if a well is in LGR and the number of this LGR if any 

    #print(f"\n wells_dates_filename\n{wells_dates_filename}")
    #print(f"\n well_names\n{well_names}")
    #print(f"\n perfs_array\n{perfs_array}")

    #print()
    #print(f"times\n{times}")
    

#    print()
#    print(startDate, date(startDate[2], startDate[1], startDate[0]))


#    for step in times:
#        print(f"step={step}, {date(startDate[2], startDate[1], startDate[0]) + timedelta(days=step)}") 
