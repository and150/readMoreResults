#-*- coding:utf-8 -*-
#indexes of vectors
i_d = {
   'Sopr' : 0, 
   'Swpr' : 1,
   'Sbhp' : 2,
   'Sopt' : 3,
   'Swpt' : 4,
   'Swit' : 5,

   'Hopr' : 6,
   'Hwpr' : 7,
   'Hbhp' : 8,
   'Hwefa': 9,

   'Swir' : 10,
   'Hwir' : 11,
   'Hopt' : 12,
   'Hwpt' : 13,
   'Hwit' : 14,
   'Sthp' : 15,
   'Hthp' : 16,

   'wPI4' : 17,
   'wut' : 18
   }

VEC = len(i_d)

LIQCUT = 0.0105 # liquid rate cut for PBU
TIMETOL = 0.0001 # 0.001
PTOL = 0.02
MONTHDELTA = 1

NBCHAR = 1   # bytes in char
NBINT = 4    # bytes in integer
NBREAL = 4   # bytes in real
NBFLOAT = 4  # bytes in float
