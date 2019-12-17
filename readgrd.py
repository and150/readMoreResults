import array
import constants as cts

def get_ijk_values_from_array(array, dimensions, connections):
    I,J,K = dimensions[0], dimensions[1], dimensions[2]
    for item in connections:
        i,j,k = item[0]-1,item[1]-1,item[2]-1
        print(item[0],item[1],item[2], array[I*J*k + I*j + i])


def read_static_arrays(input_file):

    def read_byte_array(start, end, input_file, arr_type = 'l'):
        arr = array.array(arr_type)
        arr.frombytes(input_file.read(end-start))
        return arr

    # READ GRD FILE
    s = 0
    f = 1*cts.NBINT
    number_of_header = read_byte_array(s,f, input_file)[0]

    s = f
    f = s + number_of_header*cts.NBINT 
    header = dict(zip (['nga','lkey','ltits','ltitl',
                    'nx','ny','nz', 'idgrid','ixyflo','izflow',
                    'iblkmd','2*nz+2','nLG','na',
                    'activeMaps','dpbdtFlag','drvdtFlag','coarsenFlag',
                    'mapaxesFlag','not_used'], 
                    read_byte_array(s,f, input_file)))
    print(header)

    # if any LGRs TODO test no LGR run
    num_of_LG_header = 0
    if header['nLG'] > 0: 
        s = f
        f = s + 1*cts.NBINT
        num_of_LG_header = read_byte_array(s,f, input_file)[0]
        
        for nL in range(0,header['nLG']):
            s = f
            f = s + nL*num_of_LG_header*cts.NBINT 
            LG_header = dict(zip (['nxL','nyL','nzL', 'ixl','ixu','iyl',
                                    'iyu','izl','izu','Radial flag',
                                    'Parent local grid','not used0','not used1',
                                    'Number of active cells','Pebi flag',
                                    'Maximum vertex count','not used2','not used3',
                                    'not used4','not used5'],
                            read_byte_array(s,f, input_file)))
            print(LG_header)

    lkey, ltits, ltitl = header['lkey'], header['ltits'], header['ltitl']
    nzt = lkey + ltits + ltitl

    # read array headers (nga)
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
        #print(title)
        #print(key, short_title, long_title)

        s = f
        f = s + header['2*nz+2']*cts.NBINT
        #print(f"s,f = {s},{f}, {f-s}")
        size_info_by_layer = read_byte_array(s,f, input_file)
        #grd_array_index.update({key: size_info_by_layer})
        #print(key, size_info_by_layer)
        grd_array_index.update({key: sum(list(filter(lambda x: x>0, size_info_by_layer))) })

'''
    # read requested arrays
    temp_array = []
    for item in grd_array_index:
        del temp_array[:]
        s = f
        f = s + grd_array_index[item]*cts.NBREAL
    
        out_arrays = ['DZTV','PERMX', 'PERMY']
        if item.strip() in  out_arrays:
            temp_array = read_byte_array(s,f, input_file, 'f')
            #print(item, temp_array)
            get_ijk_values_from_array(temp_array, [header['nx'],header['ny'],header['nz']],  [(60,1,k+1) for k in range(85)])        
        else:
            input_file.seek(f)
    # TODO create LGR arrays reading (necessary for ara input_file)
        
        '''
