import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime

time_midnight = datetime.time(0)
time_2am = datetime.time(2)
time_4am = datetime.time(4)
time_6am = datetime.time(6)
time_8am = datetime.time(8)
time_10am = datetime.time(10)
time_noon = datetime.time(12)
time_2pm = datetime.time(14)
time_4pm = datetime.time(16)
time_6pm = datetime.time(18)
time_8pm = datetime.time(20)
time_10pm = datetime.time(22)
time_1159pm = datetime.time(23, 59, 59)

def month_n2s(n):
    if n == 10:
        return 'Oct'
    elif n == 11:
        return 'Nov'
    elif n == 12:
        return 'Dec'
    elif n == 1:
        return 'Jan'
    elif n == 2:
        return 'Feb'
    elif n == 3:
        return 'March'
    elif n == 4:
        return 'April'
    elif n == 5:
        return 'May'
    elif n == 6:
        return 'June'
    elif n == 7:
        return 'July'
    elif n == 8:
        return 'August'
    else:
        return 'Sep'

def day_n2s(n):
    if n == 0:
        return 'Mon'
    elif n == 1:
        return 'Tue'
    elif n == 2:
        return 'Wed'
    elif n == 3:
        return 'Thu'
    elif n == 4:
        return 'Fri'
    elif n == 5:
        return 'Sat'
    else:
        return 'Sun'

def time2bin(d):
    if time_midnight <= d < time_2am:
        return 'midnight_2AM'
    elif time_2am <= d < time_4am:
        return '2AM_4AM'
    elif time_4am <= d < time_6am:
        return '4AM_6AM'
    elif time_6am <= d < time_8am:
        return '6AM_8AM'
    elif time_8am <= d < time_10am:
        return '8AM_10AM'
    elif time_10am <= d < time_noon:
        return '10AM_noon'
    elif time_noon <= d < time_2pm:
        return 'noon_2PM'
    elif time_2pm <= d < time_4pm:
        return '2PM_4PM'
    elif time_4pm <= d < time_6pm:
        return '4PM_6PM'
    elif time_6pm <= d < time_8pm:
        return '6PM_8PM'
    elif time_8pm <= d < time_10pm:
        return '8PM_10PM'
    elif time_10pm <= d <= time_1159pm:
        return '10PM_midnight'

def getProcessedData():
    do_data = pd.read_csv('../data/raw/DO data.csv')
    do_data['dt'] = do_data['year'].astype(str) + '-' + do_data['month'].astype(str) + '-' + \
                do_data['day'].astype(str) + ' ' + do_data['time']

    do_data['date'] = pd.to_datetime(do_data['dt'], errors = 'coerce')

    do_data = do_data.drop(['dt'], axis = 1)

    do_data = do_data.set_index(do_data['date'])

    do_months = do_data.month.map(lambda n : month_n2s(n))

    do_data_dayn = do_data.date.map(lambda x : x.weekday())

    do_data_days = do_data_dayn.map(lambda x : day_n2s(x))

    do_data_timebins = do_data.date.map(lambda t : time2bin(t.time()))

    do_data['month_str'] = do_months

    do_data['dayofweek_int'] = do_data_dayn

    do_data['dayofweek_str'] = do_data_days

    do_data['timebins'] = do_data_timebins

    do_data.to_csv('../data/processed/do_data_anot.csv')

    do_data['date_2'] = do_data.date.map(lambda d : d.date())

    do_data_medians = do_data.groupby('date_2').median()

    do_data_medians.to_csv('../data/processed/do_data_medians_groupedby_date.csv')

    return do_data, do_data_medians