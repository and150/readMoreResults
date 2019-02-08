# number of base vectors to read 
# 6 vectors simulated and history oil rate, water rate, pressure, cumulative oil, water, injection 
# 3 vectors simulated cumulatives oil, water, injection
# 1 history well efficiency factor (to get history cumulatives)
VEC = 6+3+1+2

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


LIQCUT = 0.0105 # отсечка по дебиту жидкости для КВД
TIMETOL = 0.001
PTOL = 0.02

NBINT = 4    # количество байт в целом числе
NBREAL = 4   # количество байт в реальном числе
NBFLOAT = 4  # количество байт в числе с пл.точкой
