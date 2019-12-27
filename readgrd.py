import array
import constants as cts

def get_ijk_values_from_array(array, dimensions, connections):
    I,J,K = dimensions[0], dimensions[1], dimensions[2]
    for item in connections:
        i,j,k = item[0]-1,item[1]-1,item[2]-1
        print(item[0],item[1],item[2], array[I*J*k + I*j + i])


def read_byte_array(start, end, input_file, arr_type = 'l'):
    arr = array.array(arr_type)
    arr.frombytes(input_file.read(end-start))
    return arr

def get_null_ranges(rvol_array):
    gap_indexes ={}
    prev_item = -999
    gap_start = False
    i, n = 0, 0
    for item in rvol_array:
        if item ==0 and prev_item !=0:
            gap_start = True
        if item !=0 and prev_item ==0:
            gap_start = False
            gap_indexes.update({i-n:n})
            n = 0
        if gap_start == True:
            n+=1
        i+=1
        prev_item = item
    return gap_indexes

def insert_gaps(target_array, gaps_dict):
    #print(gaps_dict)
    for gap in gaps_dict:
        #print(gap)
        target_array[gap:gap] = list(x*0 for x in range(gaps_dict[gap]))
    #print(f"after= {target_array}")
    return target_array



# READ GRD FILE
def read_static_arrays(input_file, out_arrays_names):

    s = 0
    f = 1*cts.NBINT
    number_of_header = read_byte_array(s,f, input_file)[0]
    #print(f"number_of_header={number_of_header}") # debug

    s = f
    f = s + number_of_header*cts.NBINT 
    header = dict(zip (['nga','lkey','ltits','ltitl',
                    'nx','ny','nz', 'idgrid','ixyflo','izflow',
                    'iblkmd','2*nz+2','nLG','na',
                    'activeMaps','dpbdtFlag','drvdtFlag','coarsenFlag',
                    'mapaxesFlag','not_used'], 
                    read_byte_array(s,f, input_file)))
    #print(header)


    # if any LGRs
    LG_names = []
    LG_header =[] 
    if header['nLG'] > 0: 
        s = f
        f = s + 1*cts.NBINT
        num_of_LG_header = read_byte_array(s,f, input_file)[0]
        #print(f"num_of_LG_header={num_of_LG_header}") # debug

        for nL in range(1,header['nLG']+1):
            s = f
            f = s + num_of_LG_header*cts.NBINT 
            curr_LG_header = dict(zip (['nxL','nyL','nzL', 'ixl','ixu','iyl',
                                    'iyu','izl','izu','Radial flag',
                                    'Parent local grid','not used0','not used1',
                                    'Number of active cells','Pebi flag',
                                    'Maximum vertex count','not used2','not used3',
                                    'not used4','not used5'],
                            read_byte_array(s,f, input_file)))
            s = f
            f = s + 64*cts.NBCHAR 
            LG_names.append(array.array.tobytes(read_byte_array(s,f, input_file,'b')))
            LG_header.append(curr_LG_header)
    #print(f"LG_names={LG_names} LG_header={LG_header}")  # debug

    lkey, ltits, ltitl = header['lkey'], header['ltits'], header['ltitl']
    nzt = lkey + ltits + ltitl

    # read main arrays headers (nga)
    grd_array_index = {}
    for nga in range(0, header['nga']):
        s = f
        f = s + lkey*cts.NBCHAR
        key = array.array.tobytes(read_byte_array(s,f, input_file,'b')).decode("utf-8")

        s = f
        f = s + ltits*cts.NBCHAR
        short_title = array.array.tobytes(read_byte_array(s,f, input_file,'b'))

        s = f
        f = s + ltitl*cts.NBCHAR
        long_title = array.array.tobytes(read_byte_array(s,f, input_file,'b'))

        #title = list(map((lambda x: x.decode("utf-8")), [key,short_title, long_title])) 
        #print(title,"\n",key, short_title, long_title) # debug

        s = f
        f = s + header['2*nz+2']*cts.NBINT
        #print(f"s,f = {s},{f}, {f-s}") # debug
        size_info_by_layer = read_byte_array(s,f, input_file)
        #print(size_info_by_layer)
        grd_array_index.update({key: sum(list(filter(lambda x: x>0, size_info_by_layer[:-2]))) }) # remove 2 last elements in index header !!!
    #print(f"grd_array_index={grd_array_index}")


    # TODO need to be refactored (make one cycle for Main grid and for all LGRs if it is possible...
    out_arrays = []
    grid_dimensions = [[header['nx'], header['ny'], header['nz']]]
    # read requested arrays from main grid
    main_grid_arrays = {} 
    temp_array = []
    gaps_dict = {}
    for item in grd_array_index:
        del temp_array[:]
        s = f

        if item.strip() in ['RVOL','XGRI','YGRI','ZGRI']:
            f = s + grd_array_index[item]*cts.NBREAL
        else:
            if header['activeMaps'] == 1:
                f = s + header['na']*cts.NBREAL
            else:
                f = s + grd_array_index[item]*cts.NBREAL

        if header['activeMaps'] == 1 and item.strip() == 'RVOL':
            gaps_dict = get_null_ranges(read_byte_array(s,f, input_file, 'f'))

        if item.strip() in out_arrays_names:  # outputs only requested array plus RVOL
            temp_array = read_byte_array(s,f, input_file, 'f')
            main_grid_arrays.update({item.strip():insert_gaps(list(temp_array), gaps_dict)})
        else:
            input_file.seek(f)
    out_arrays.append(main_grid_arrays)        


    #TODO active maps support for LGR (it seems that I'v done it for main grid (need to test)) !!!
    # read requested LGR arrays
    if header['nLG'] > 0:
        for LG in range(header['nLG']):
            LG_grid_arrays = {}
            for item in grd_array_index:
                del temp_array[:]
                s = f

                if item.strip() in ['XGRI','YGRI','ZGRI']:
                    f = s + 4*LG_header[LG]['nxL']*LG_header[LG]['nyL']*2*LG_header[LG]['nzL']*cts.NBREAL
                else:
                    f = s + LG_header[LG]['nxL']*LG_header[LG]['nyL']*LG_header[LG]['nzL']*cts.NBREAL

                if item.strip() in  out_arrays_names:  # outputs only requested array
                #if True:
                    temp_array = read_byte_array(s,f, input_file, 'f')
                    LG_grid_arrays.update({item.strip():[*temp_array]})
                else:
                    input_file.seek(f)
            out_arrays.append(LG_grid_arrays)
            grid_dimensions.append([LG_header[LG]['nxL'], LG_header[LG]['nyL'], LG_header[LG]['nzL']])

    return [out_arrays, grid_dimensions]
