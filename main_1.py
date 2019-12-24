# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import function_1 as func
import matplotlib.pyplot as plt
import datetime


# Get unique MID list
MID = func.get_mid(r'C:\Users\lkr\Desktop\graduate\previous_data\RTDMD_150101.csv')

# plot trend chart(pressure)
date_list = ['2015-01-01']
data = pd.DataFrame()
for date in date_list:
    data = pd.concat([data, func.process_data(date, '13300000054-0-8')], axis=0)
plt.legend()
plt.title('Pressure time series')
plt.show()


# Train Model
def train(k, date_range, sample_point):
    train_1 = func.spectral_clustering_1(func.similarity_matrix_1(date_range, sample_point[:]), sample_point, k)
    mode_list_1 = func.daily_trend_mode_1(k, train_1, date_range, sample_point[:])
    train_2 = func.spectral_clustering_2(func.similarity_matrix_2(mode_list_1), sample_point, k)
    mode_list_2 = func.daily_trend_mode_2(k, train_2, mode_list_1)
    return mode_list_2


# Daily pressure trend mode(13300000054-0-8, 2015)
k = 7
sample_point = ['13300000054-0-8']
date_range = func.create_assist_date('2015-01-01', '2015-12-31')
mode_list = train(k, date_range, sample_point)

data = pd.DataFrame()
for date in mode_list[:, 2]:
    data = pd.concat([data, func.process_data(date, '13300000054-0-8')], axis=0)
    plt.legend()
    plt.title('Mode pressure time series(13300000054-0-8, 2015)')
    plt.show()

# Daily pressure trend mode(2015)
k = 7
sample_point = MID
date_range = func.create_assist_date('2015-01-01', '2015-12-31')
mode_list = train(k, date_range, sample_point)

data = pd.DataFrame()
for date in mode_list[:, 2]:
    for point in mode_list[:, 1]:
        data = pd.concat([data, func.process_data(date, point)], axis=0)
        plt.legend()
        plt.title('Mode pressure time series(2015)')
        plt.show()


# Match daily trend with modes
def match(date, sample_point, mode_list):
    length = len(mode_list)
    s_matrix = np.zeros(shape=(length, 1))
    for a in range(length):
        s_matrix[a] = func.dtw_distance(func.process_data(mode_list[a, 1], mode_list[a, 2]).PRESSURE,
                                        func.process_data(date, sample_point).PRESSURE)
    s_matrix[np.isnan(s_matrix)] = 999
    mode = np.where(s_matrix.min())
    return mode


# Accident-mode match(2015/04/08)
date = '2015-04-08'
sample_point = '13300000039-0-8'
mode = match(date, sample_point, mode_list)
data_acc = func.process_data(date, sample_point)
data_mode = func.process_data(mode_list[mode, 1], mode_list[mode, 2])
plt.plot(data_acc.hour, data_acc.PRESSURE, 'blue', label='leak time series')
plt.plot(data_mode.hour, data_mode.PRESSURE, 'yellow', label='typical time series')
plt.legend()
plt.show()

# Accident-mode match collection
data_accident = pd.read_csv(r'C:\Users\lkr\Desktop\graduate\previous_data\accident_2015.csv')
sample_point = data_accident.MID
pd.to_datetime(data_accident['CREATETIME'])
date = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in data_accident['CREATETIME']]
accident_list = [date, sample_point]
match_mode = []
for acc in accident_list:
    date = acc[1]
    sample_point = acc[2]
    match_mode = [match_mode, mode_list[match(date, sample_point, mode_list)]]
match_mode = pd.Series(match_mode, index=['matches'])
acc_match_collection = match_mode.value_counts()
risky_mode = pd.concat(mode_list[acc_match_collection[1, 1]], mode_list[acc_match_collection[2, 1]])


# Anomaly Detection
def detection(date, sample_point, mode_list, risky_mode):
    mode = match(date, sample_point, mode_list)
    if mode_list[mode].isin(risky_mode):
        print('Warning')
    else:
        print('Safe')
    return mode
