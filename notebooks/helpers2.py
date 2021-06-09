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
        return 'Oct, 29.9 (2004) / 30.7 (2005)'
    elif n == 11:
        return 'Nov, 26.3 (2004) / 27.8 (2005)'
    elif n == 12:
        return 'Dec, 21.8 (2004) / 23 (2005)'
    elif n == 1:
        return 'Jan, 19.5 (2005) / 20 (2006)'
    elif n == 2:
        return 'Feb, 20.7 (2005), / 22.7 (2006)'
    elif n == 3:
        return 'March, 23.8 (2005)'
    elif n == 4:
        return 'April, 28 (2005)'
    elif n == 5:
        return 'May, 31.6 (2005)'
    elif n == 6:
        return 'June, 33.4 (2005)'
    elif n == 7:
        return 'July, 35.3 (2005)'
    elif n == 8:
        return 'August, 35.7 (2005)'
    else:
        return 'Sep, 33.4 (2005)'

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
        return 0
    elif time_2am <= d < time_4am:
        return 1
    elif time_4am <= d < time_6am:
        return 2
    elif time_6am <= d < time_8am:
        return 3
    elif time_8am <= d < time_10am:
        return 4
    elif time_10am <= d < time_noon:
        return 5
    elif time_noon <= d < time_2pm:
        return 6
    elif time_2pm <= d < time_4pm:
        return 7
    elif time_4pm <= d < time_6pm:
        return 8
    elif time_6pm <= d < time_8pm:
        return 9
    elif time_8pm <= d < time_10pm:
        return 10
    elif time_10pm <= d <= time_1159pm:
        return 11

def bin2s(d):
    if d == 0:
        return 'midnight_2AM'
    elif d == 1:
        return '2AM_4AM'
    elif d == 2:
        return '4AM_6AM'
    elif d == 3:
        return '6AM_8AM'
    elif d == 4:
        return '8AM_10AM'
    elif d == 5:
        return '10AM_noon'
    elif d == 6:
        return 'noon_2PM'
    elif d == 7:
        return '2PM_4PM'
    elif d == 8:
        return '4PM_6PM'
    elif d == 9:
        return '6PM_8PM'
    elif d == 10:
        return '8PM_10PM'
    elif d == 11:
        return '10PM_midnight'


def cleanDates(do_data):
    do_data['dt'] = do_data['year'].astype(str) + '-' + do_data['month'].astype(str) + '-' + \
                do_data['day'].astype(str) + ' ' + do_data['time']

    do_data['date_time'] = pd.to_datetime(do_data['dt'], errors = 'coerce')

    do_data['date'] = do_data.date_time.map(lambda t : t.date())

    do_data['time'] = do_data.date_time.map(lambda t : t.time())

    do_data = do_data.drop(['dt'], axis = 1)

    do_data = do_data.set_index(do_data['date_time'])

    do_data = do_data.drop(['date_time'], axis = 1) #remove later if necessary

    do_data['month_str'] = do_data.month.map(lambda n : month_n2s(n))

    do_data['dayofweek_int'] = do_data.index.map(lambda x : x.weekday())

    do_data['dayofweek_str'] = do_data.dayofweek_int.map(lambda x : day_n2s(x))

    do_data['timebins_int'] = do_data.index.map(lambda t : time2bin(t.time()))

    do_data['timebins_str'] = do_data.timebins_int.map(lambda t : bin2s(t))

    return do_data

def getGroupByObj(do_data):
        
    do_data_day = do_data.groupby('date')

    do_data_month = do_data.groupby('month')

    do_data_dayOfWeek = do_data.groupby('dayofweek_int')

    do_data_timeBins = do_data.groupby('timebins_int')

    do_data_monthTimeBins = do_data.groupby(['month', 'timebins_int'])

    return do_data_day, do_data_month, do_data_dayOfWeek, do_data_timeBins, do_data_monthTimeBins

def getDataAndSummary(path = '../data/raw/DO data.csv'):
    do_data = pd.read_csv(path)
    
    do_data = cleanDates(do_data)

    do_data_day, do_data_month, do_data_dayOfWeek, do_data_timeBins, do_data_monthTimeBins = getGroupByObj(do_data)

    do_data.to_csv('../data/processed/do_data_anot.csv')

    do_data.describe().drop(columns = ['day', 'month', 'year', 'dayofweek_int', 'timebins_int']).to_csv('../summary/descriptive_stats/do_data.csv')
    
    do_data_day.describe().drop(columns = ['day', 'month', 'timebins_int', 'dayofweek_int', 'year']).to_csv('../summary/descriptive_stats/do_data_groupedby_date.csv')

    do_data_month.describe().drop(columns = ['year', 'day', 'dayofweek_int', 'timebins_int']).to_csv('../summary/descriptive_stats/do_data_groupedby_month.csv')

    do_data_dayOfWeek.describe().drop(columns = ['day', 'month', 'year', 'timebins_int']).to_csv('../summary/descriptive_stats/do_data_groupedby_dayOfWeek.csv')

    do_data_timeBins.describe().drop(columns = ['day', 'month', 'year', 'dayofweek_int']).to_csv('../summary/descriptive_stats/do_data_groupedby_timeBins.csv')

    do_data_monthTimeBins.describe().drop(columns = ['day', 'year', 'dayofweek_int']).to_csv('../summary/descriptive_stats/do_data_groupedby_monthTimeBins.csv')    

    #add descriptive statistics to appropriate directories summary

    #add medians to appropariate directories data

    return do_data, do_data_day, do_data_month, do_data_dayOfWeek, do_data_timeBins, do_data_monthTimeBins

    # do_data_month_medians = do_data_month.median()

    # do_data_dow_medians = do_data_dow.median()

    # do_data_tb_medians = do_data_tb.median()

    # do_data_mtb_medians = do_data_mtb.median()

