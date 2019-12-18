from datetime import  date, datetime, timedelta

def get_wells_cells(out_arrays, wells_dates_filename, well_names, perfs_array, times, start_date):

    wells_dates_from_file = [[x.split()[0], datetime.strptime(' '.join(x.split()[1:]), "%d.%m.%Y %H:%M:%S")] for x in [line.rstrip('\n') for line in open(wells_dates_filename)]]
    #print(wells_dates_from_file)

    dates = [date(start_date[2], start_date[1], start_date[0]) + timedelta(days=x) for x in times]
    #print(dates)


    #TODO choose dates_from_file form dates



    #print(f"out_arrays\n{out_arrays}")
    #print()
    #print(f"wells_dates_filename\n{wells_dates_filename}")
    #print()
    #print(f"well_names\n{well_names}")
    #print()
    #print(f"perfs_array\n{perfs_array}")

    #print()
    #print(f"times\n{times}")
    

#    print()
#    print(startDate, date(startDate[2], startDate[1], startDate[0]))


#    for step in times:
#        print(f"step={step}, {date(startDate[2], startDate[1], startDate[0]) + timedelta(days=step)}") 
