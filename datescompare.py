import  datetime
#сравнение даты(строка) со временем (дни в формате float)
def DatesCompare(sdate="31.12.2001 00:00:00", time=0.0, sdatArr=[]):
    SDAT = datetime.datetime.strptime(str(sdatArr[2])+"-"+str(sdatArr[1])+"-"+str(sdatArr[0]),"%Y-%m-%d")
    date = datetime.datetime.strptime(sdate,"%d.%m.%Y %H:%M:%S")
    time1 = date - SDAT
    time1= time1.days + time1.seconds/60/60/24
    return time - time1

def date2days(sdate="31.12.2001 00:00:00", sDate = []):
#функция берет дату в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС конвертирует ее в дни и 
# вычитает из нее дату начала расчетов чтобы сравнивать с массивом времен временных шагов из RATE-файла    
    initDate = datetime.datetime.strptime(str(sDate[2])+"-"+str(sDate[1])+"-"+str(sDate[0]),"%Y-%m-%d")  # конвертация стартовой даты из массива во время   
    date = datetime.datetime.strptime(sdate,"%d.%m.%Y %H:%M:%S")    # конвертация даты из формата ДД.ММ.ГГГГ ЧЧ:ММ:СС во время
    time = date - initDate    # расчет интервала времени от начала расчета
    time =   time.days + time.seconds/60/60/24 # перевод временного интервала в дни
    return time



