import pandas as pd
import numpy as np
import datetime
import function_2 as func_2
import main_1
import matplotlib.pyplot as plt
from pyheatmap.heatmap import HeatMap


# Get accident location and plot scatter diagram and heat map
acc_origin_path = r'C:/Users/lkr/Desktop/graduate/previous_data/accident_2015.csv'  # path for address descriptions
acc_new_path = r'C:/Users/lkr/Desktop/graduate/previous_data/accident_longitude_latitude.csv'  # path for longitudes and latitudes
func_2.get_location(acc_origin_path, acc_new_path)
acc_location = pd.read_csv(r'C:/Users/lkr/Desktop/graduate/previous_data/accident_longitude_latitude.csv')
plt.scatter(acc_location, s=20, c='b')  # plot scatter diagram
hm = HeatMap(acc_location)  # plot heat map
hm.clickmap(save_as='hit.png')
hm.heatmap(save_as='heat.png')

# Accidents-Sample points match
sp_location = pd.read_csv(r'C:/Users/lkr/Desktop/graduate/previous_data/sample_points_location.csv')
sp_match = []
for i in acc_location:
    dist = 99999
    sp = [-1, -1]
    for j in sp_location:
        if dist > func_2.mhd_distance(i, j) > 0.001:
            dist = func_2.mhd_distance(i, j)
            sp = j
    sp_match = [sp_match, sp]
    sp_match = pd.DataFrame(sp_match)

# Calculate Page Rank Value
acc_data = pd.read_csv(acc_origin_path)
pd.to_datetime(acc_data['CREATETIME'])
acc_data['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in acc_data['CREATETIME']]
acc_data['effect_time_limit'] = acc_data['datetime'] + datetime.timedelta(days=1)
acc_data['location'] = sp_match
effect_matrix = np.zeros(len(sp_location))
for i in range(len(sp_location)):
    for j in range(len(sp_location)):
        if acc_data[i].effect_time_limit > acc_data[j].datetime > acc_data[i].datetime:
            effect_matrix[i, j] += 1
pr = func_2.pagerank(effect_matrix)

# Find high-PR sample points
sig_high_limit = 6
represent_point = pr.max(sig_high_limit)
represent_point = [represent_point, acc_data[np.where(pr.max(sig_high_limit))]]
represent_point = pd.DataFrame(represent_point)

# Plot the high-PR points in the scatter plot
plt.scatter(acc_location, 'blue', represent_point.location, 'orange')

# Generate clusters
cluster = []
cluster_no = -1
for i in sp_location:
    dist = 9999
    for j in represent_point.location:
        if dist > func_2.mhd_distance(i, j):
            dist = func_2.mhd_distance(i, j)
            cluster_no = represent_point['location'].find(j)
    cluster = [cluster, cluster_no]
sp_cluster = [sp_location.MID, cluster]
sp_cluster = pd.DataFrame(sp_cluster)

# Numbers of sample points and accidents in each cluster
sp_num = sp_cluster['cluster'].value_counts()
acc_cluster = [sp_match, sp_cluster[np.where(sp_match['MID'] == sp_cluster['MID'])]]
acc_cluster = pd.DataFrame(acc_cluster)
acc_num = acc_cluster['cluster'].value_counts()

# Train the initial model(for 6 represent points)
mode_list_rp, risky_mode_rp = func_2.train_rp(6, represent_point.MID, acc_data)

# Train the models(for each risky clusters)
mode_list_1, risky_mode_1 = func_2.train_cluster(8, '13300000068-0-8', sp_cluster, acc_data)
mode_list_2, risky_mode_2 = func_2.train_cluster(6, '13300000050-3', sp_cluster, acc_data)
mode_list_3, risky_mode_3 = func_2.train_cluster(8, '18013104570-01', sp_cluster, acc_data)
mode_list_4, risky_mode_4 = func_2.train_cluster(4, '13300000020-0', sp_cluster, acc_data)
mode_list_5, risky_mode_5 = func_2.train_cluster(7, '13300000025-0-8', sp_cluster, acc_data)
mode_list_6, risky_mode_6 = func_2.train_cluster(3, '13300000004-0-9', sp_cluster, acc_data)

# First anomaly detection()
date = '2015-01-17'
for i in represent_point.MID:
    main_1.detection(date, i, mode_list_rp, risky_mode_rp)

# Second anomaly detection(if needed)
date = '2015-01-17'
anomaly_cluster_no = 5
for i in sp_cluster[np.where(sp_cluster.MID == represent_point[5].MID)].MID:
    main_1.detection(date, i, mode_list_5, risky_mode_5)
