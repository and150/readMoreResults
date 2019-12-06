#-*- coding:utf-8 -*-
# number of base vectors to read 
# 6 vectors simulated and history oil rate, water rate, pressure, cumulative oil, water, injection 
# 3 vectors simulated cumulatives oil, water, injection
# 1 history well efficiency factor (to get history cumulatives)
VEC = 6 + 3 + 1 + 2 + 3 + 2

#indexes of vectors
Sopr  = 0
Swpr  = 1
Sbhp  = 2
Sopt  = 3
Swpt  = 4
Swit  = 5

Hopr  = 6
Hwpr  = 7
Hbhp  = 8

Hwefa = 9

Swir  = 10
Hwir  = 11

Hopt  = 12
Hwpt  = 13
Hwit  = 14

Sthp  = 15
Hthp  = 16

LIQCUT = 0.0105 # liquid rate cut for PBU
TIMETOL = 0.0001 # 0.001
PTOL = 0.02
MONTHDELTA = 1

NBINT = 4    # bytes in integer
NBREAL = 4   # bytes in real
NBFLOAT = 4  # bytes in float
