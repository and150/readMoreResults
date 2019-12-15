import array
import constants as cts

def read_static_arrays(file):

    def read_byte_array(start, end, file, arr_type = 'l'):
        arr = array.array(arr_type)
        arr.frombytes(file.read(end-start))
        return arr

    # READ GRD FILE
    s = 0
    f = 1*cts.NBINT
    number_of_header = read_byte_array(s,f, file)[0]

    s = f
    f = s + number_of_header*cts.NBINT 
    header = dict(zip (['nga','lkey','ltits','ltitl',
                    'nx','ny','nz', 'idgrid','ixyflo','izflow',
                    'iblkmd','2*nz+2','nLG','na',
                    'activeMaps','dpbdtFlag','drvdtFlag','coarsenFlag',
                    'mapaxesFlag','not_used'], 
                    read_byte_array(s,f, file)))
    #print(header)

    # if any LGRs TODO test no LGR run
    num_of_LG_header = 0
    if header['nLG'] > 0: 
        s = f
        f = s + 1*cts.NBINT
        num_of_LG_header = read_byte_array(s,f, file)[0]
        
        for nL in range(0,header['nLG']):
            s = f
            f = s + nL*num_of_LG_header*cts.NBINT 
            LG_header = dict(zip (['nxL','nyL','nzL', 'ixl','ixu','iyl',
                                    'iyu','izl','izu','Radial flag',
                                    'Parent local grid','not used0','not used1',
                                    'Number of active cells','Pebi flag',
                                    'Maximum vertex count','not used2','not used3',
                                    'not used4','not used5'],
                            read_byte_array(s,f, file)))
            #print(LG_header)

    nzt = header['lkey']+header['ltits']+header['ltitl']


# TODO now file is read sequentally, it is nesessary to realize random access (map file first)
    nga = 5 
    f = 1*cts.NBINT + number_of_header*cts.NBINT + \
        header['nLG']*(1*cts.NBINT+num_of_LG_header*cts.NBINT)
    #print(f)

    s = f + nga*nzt*cts.NBCHAR + nga*header['2*nz+2']*cts.NBINT 
    f = s + nzt*cts.NBCHAR
    array_title = array.array.tobytes(read_byte_array(s,f, file,'b'))
    print(array_title)
    print(f"s,f = {s},{f}, {f-s}")
    s = f
    f = s + header['2*nz+2']*cts.NBINT
    size_info_by_layer = read_byte_array(s,f, file)
    print(size_info_by_layer)
    print(f"s,f = {s},{f}, {f-s}")
    print("next")

'''
    for nga in range(1, header['nga']):
        s = f
        f = s + nzt*cts.NBCHAR
        print(f"s,f = {s},{f}, {f-s}")
        array_title = array.array.tobytes(read_byte_array(s,f, file,'b'))
        
        s = f
        f = s + header['2*nz+2']*cts.NBINT
        print(f"s,f = {s},{f}, {f-s}")
        print("next")
        size_info_by_layer = read_byte_array(s,f, file)

        #print(array_title)
        #print(size_info_by_layer)
'''
