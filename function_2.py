import csv
import json
import time
from bs4 import BeautifulSoup
import requests
import numpy as np
import function_1 as func_1
import main_1
import matplotlib.pyplot as plt
import pandas as pd
import datetime


# Get longitude and latitude based on address of accidents
def get_location(origin_path, new_path):
    url_geocode = r'http://api.map.baidu.com/geocoder/v2/?'  # url of Baidu Map API
    AK = ['oFCSeioUzdN5NfzSlBBXqBEfXgp26mGM', 'Akqk5xjbSGzy1WC1IUF04K2CQWGtOFNv', 'HCdq1Ry35rwgVQwjAXqAEQGzWNY7pi1h',
          'GtOZERwlG0PynPwFrBYaF9wWcAGxvaw8', 'iRKkZehZimIWdGoxfjlbtLrYb0VVgVaD', 'gG0KIBhAGpAVvaRUlwFjmOtsTKGRK2tf',
          'CSsyosiklqyYUDNnBP0BR63fa9BzCHFf', 'mq4TZshHveVqML3icCC6AWnS25rbjYBz', 'rBYetA6WQNOlXtQWInz8ckRE0iCDsUjB',
          'QUshHD8KUAk8y9gLwDhQ6RyOgQxEB8VD', '7Ict6oZmpAYYXMjha2Tk5g4ENTCYwx03']  # key for processing
    cod = r'&ret_coordtype=bd09ll'  # longitude and latitude format
    machine_data = csv.reader(open(origin_path, 'r', encoding='utf-8'))  # get original address description
    n = 0
    akn = 0
    column_names = 'Number Type1 Accuracy1 Longitude Latitude Name Type2 Accuracy2 Longitude_2 Latitude_2 Address ' \
                   'Point Accuracy Best_Longitude Best_Latitude Best_Type Best_Address '
    with open(new_path, 'a', encoding='utf-8') as f:  # Write new indexes into the new file
        f.write(column_names)
        f.write('\n')
        f.close()
    while True:
        try:
            for addr in machine_data:
                province = str(addr[0])
                city = str(addr[1])
                mac = str(addr[2])
                wd = str(addr[3])
                anz = str(addr[4])
                anz_type = str(addr[5])
                add1 = province + city + wd
                add2 = province + city + anz
                if akn < len(AK):
                    n += 1
                    aknd = AK[akn]
                    ak = r'&output=json&ak=' + aknd
                    address1 = r'address=' + add1
                    tar_url = url_geocode + address1 + ak + cod
                    response = requests.get(url=tar_url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    response.close()
                    dictinfo = json.loads(str(soup))
                    status = dictinfo['status']
                    print(status)
                    if status == 0:
                        lng1 = round(dictinfo['result']['location']['lng'], 8)
                        lat1 = round(dictinfo['result']['location']['lat'], 8)
                        precise1 = dictinfo['result']['precise']
                        confidence1 = dictinfo['result']['confidence']
                        geocode1 = str(precise1) + ' ' + str(confidence1) + ' ' + str(lat1) + ' ' + str(
                            lng1) + ' ' + add1
                    elif status == 302 or status == 210:
                        akn += 1
                        lat1 = 'break'
                        lng1 = 'break'
                        precise1 = 0
                        confidence1 = 0
                        geocode1 = '0 0 break break ' + add1
                    else:
                        lat1 = 'na'
                        lng1 = 'na'
                        precise1 = 0
                        confidence1 = 0
                        geocode1 = '0 0 na na ' + add1
                    address2 = r'address=' + add2
                    tar_url2 = url_geocode + address2 + ak + cod
                    response2 = requests.get(url=tar_url2)
                    soup2 = BeautifulSoup(response2.content, 'html.parser')
                    response2.close()
                    dictinfo2 = json.loads(str(soup2))
                    status2 = dictinfo2['status']
                    print(status2)
                    if status2 == 0:
                        lng2 = round(dictinfo2['result']['location']['lng'], 8)
                        lat2 = round(dictinfo2['result']['location']['lat'], 8)
                        precise2 = dictinfo2['result']['precise']
                        confidence2 = dictinfo2['result']['confidence']
                        geocode2 = str(precise2) + ' ' + str(confidence2) + ' ' + str(lat2) + ' ' + str(
                            lng2) + ' ' + add2
                    elif status2 == 302 or status2 == 210:
                        akn += 1
                        precise2 = 0
                        confidence2 = 0
                        lat2 = 'break'
                        lng2 = 'break'
                        geocode2 = '0 0 break break ' + add2
                    else:
                        lat2 = 'na'
                        lng2 = 'na'
                        precise2 = 0
                        confidence2 = 0
                        geocode2 = '0 0 na na ' + add2
                    if anz_type == 'on spot':
                        if precise1 == 1:
                            geocode3 = str(precise1) + ' ' + str(confidence1) + ' ' + str(lat1) + ' ' + str(
                                lng1) + ' ' + anz_type + ' point'
                        elif precise1 == 0 and precise2 == 0:
                            geocode3 = str(precise1) + ' ' + str(confidence1) + ' ' + str(lat1) + ' ' + str(
                                lng1) + ' ' + anz_type + ' point'
                        else:
                            geocode3 = str(precise2) + ' ' + str(confidence2) + ' ' + str(lat2) + ' ' + str(
                                lng2) + ' ' + anz_type + ' Address'
                    else:
                        geocode3 = str(precise2) + ' ' + str(confidence2) + ' ' + str(lat2) + ' ' + str(
                            lng2) + ' ' + anz_type + ' Address'
                    geocode = mac + ' ' + geocode1 + ' ' + geocode2 + ' ' + geocode3
                    with open(new_path, 'a', encoding='utf-8') as f:
                        f.write(geocode)
                        f.write('\n')
                        f.close()
                    print('good' + str(n))
                else:
                    print('Not enough ak')
                    break
            print('Complete')
        except:
            print('Error')
            time.sleep(5)
            with open(new_path, 'a', encoding='utf-8') as f:
                f.write('Error')
                f.write('\n')
                f.close()
            continue
        print('End')
        break


# Manhattan distance
def mhd_distance(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


# Page Rank
def graphmove(a):
    b = np.transpose(a)
    c = np.zeros((a.shape), dtype=float)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            c[i][j] = a[i][j] / (b[j].sum())
    return c


def firstpr(c):
    pr = np.zeros((c.shape[0], 1), dtype=float)
    for i in range(c.shape[0]):
        pr[i] = float(1) / c.shape[0]
    return pr


def cal_pr(p, m, v):
    while (v == p * np.dot(m, v) + (1 - p) * v).all() == False:
        # print v
        v = p * np.dot(m, v) + (1 - p) * v
        # print (v == p*dot(m,v) + (1-p)*v).all()
    return v


def pagerank(data):
    M = graphmove(data)
    pr = firstpr(M)
    p = 0.85
    return cal_pr(p, M, pr)


# Train clusters
# Train represent points
def train_rp(k, represent_points, acc_data):
    date_range = func_1.create_assist_date('2015-01-01', '2015-12-31')
    mode_list = main_1.train(k, date_range, represent_points)

    data = pd.DataFrame()
    for date in mode_list[:, 2]:
        for point in mode_list[:, 1]:
            data = pd.concat([data, func_1.process_data(date, point)], axis=0)
            plt.legend()
            plt.title('Mode pressure time series(6 represent points, 2015)')
            plt.show()

    data_accident = acc_data
    sample_point = data_accident.MID
    pd.to_datetime(data_accident['CREATETIME'])
    date = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in data_accident['CREATETIME']]
    accident_list = [date, sample_point]
    match_mode = []
    for acc in accident_list:
        date = acc[1]
        sample_point = acc[2]
        match_mode = [match_mode, mode_list[main_1.match(date, sample_point, mode_list)]]
    match_mode = pd.Series(match_mode, index=['matches'])
    acc_match_collection = match_mode.value_counts()
    risky_mode = pd.concat(mode_list[acc_match_collection[1, 1]], mode_list[acc_match_collection[2, 1]])
    return mode_list, risky_mode


# Train each cluster
def train_cluster(k, represent_sp_mid, sp_cluster, acc_data):
    sample_point = sp_cluster[np.where(sp_cluster.MID == represent_sp_mid)].MID
    date_range = func_1.create_assist_date('2015-01-01', '2015-12-31')
    mode_list = main_1.train(k, date_range, sample_point)

    data = pd.DataFrame()
    for date in mode_list[:, 2]:
        for point in mode_list[:, 1]:
            data = pd.concat([data, func_1.process_data(date, point)], axis=0)
            plt.legend()
            plt.title('Mode pressure time series(6 represent points, 2015)')
            plt.show()

    data_accident = acc_data
    sample_point = data_accident.MID
    pd.to_datetime(data_accident['CREATETIME'])
    date = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in data_accident['CREATETIME']]
    accident_list = [date, sample_point]
    match_mode = []
    for acc in accident_list:
        date = acc[1]
        sample_point = acc[2]
        match_mode = [match_mode, mode_list[main_1.match(date, sample_point, mode_list)]]
    match_mode = pd.Series(match_mode, index=['matches'])
    acc_match_collection = match_mode.value_counts()
    risky_mode = pd.concat(mode_list[acc_match_collection[1, 1]], mode_list[acc_match_collection[2, 1]])
    return mode_list, risky_mode
