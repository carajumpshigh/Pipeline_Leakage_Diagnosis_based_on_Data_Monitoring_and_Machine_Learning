import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import linalg as LA
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize


# Generate date list
def create_assist_date(datestart=None, dateend=None):
    if datestart is None:
        datestart = '2015-01-01'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')

    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    return date_list


# Collect unique MID list
def get_mid(smp_address):
    data_smp = pd.read_csv(smp_address)
    mid = data_smp.drop_duplicates(['MID']).MID
    mid.index = range(len(mid))
    return mid


# Generate and plot daily trend of single sample point(hour based)
def process_data(date, sample_point):
    data_new = pd.read_csv(r'C:\Users\lkr\Desktop\graduate\previous_data\RTDMD_'
                           + date[2:4] + date[5:7] + date[8:10] + '.csv')
    data_new.PRESSURE = (data_new.PRESSURE - 114.6) / 3
    data_new = data_new[data_new.MID == sample_point]
    pd.to_datetime(data_new['CREATETIME'])
    data_new['datetime'] = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in data_new['CREATETIME']]
    data_new['hour'] = data_new['datetime'].apply(lambda x: x.hour)
    data_new.index = data_new['datetime']
    # data_new = data_new[date]
    data_new = data_new.resample('H').mean()
    plt.plot(data_new.hour, data_new.PRESSURE, label=date)
    data_new = data_new[['TEMPERATURE', 'PRESSURE', 'hour']]
    return data_new


# DTW
def dtw_distance(ts_a, ts_b, d=lambda x, y: abs(x - y), mww=10000):
    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))

    # Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
        cost[i, 0] = cost[i - 1, 0] + d(ts_a[i], ts_b[0])

    for j in range(1, N):
        cost[0, j] = cost[0, j - 1] + d(ts_a[0], ts_b[j])

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i - mww), min(N, i + mww)):
            choices = cost[i - 1, j - 1], cost[i, j - 1], cost[i - 1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])

    # Return DTW distance given window
    return cost[-1, -1]


# First Clustering(for each sample point)
# Distance Matrix
def similarity_matrix_1(d_list, sample_point):
    length = len(d_list)
    s_matrix = np.zeros(shape=(length, length))
    for a in range(length):
        for b in range(a):
            s_matrix[a, b] = dtw_distance(process_data(d_list[a], sample_point).PRESSURE,
                                          process_data(d_list[b], sample_point).PRESSURE)
            s_matrix[b, a] = s_matrix[a, b]
    s_matrix[np.isnan(s_matrix)] = 999
    return s_matrix


# Spectral Clustering
def spectral_clustering_1(s_matrix, points, k):
    Dn = np.diag(np.power(np.sum(s_matrix, axis=1), -0.5))
    L = np.eye(len(points)) - np.dot(np.dot(Dn, s_matrix), Dn)
    eigvals, eigvecs = LA.eig(L)
    indices = np.argsort(eigvals)[:k]
    k_smallest_eigenvectors = normalize(eigvecs[:, indices])
    #    distance = s_matrix.sum()
    return KMeans(n_clusters=k).fit_predict(k_smallest_eigenvectors)


# Generate daily trend mode for the clusters
def daily_trend_mode_1(k, train, d_list, sample_point):
    mode_list = []
    for n in range(k):
        k_type = np.array(d_list)[np.where(train == n)].tolist()
        mode_list_new = [sample_point,
                         np.array(k_type)[np.where(similarity_matrix_1(k_type, sample_point).sum(axis=0).min())].tolist()]
        mode_list = mode_list + mode_list_new
    return mode_list


# Second Clustering(for all points)
# Distance Matrix
def similarity_matrix_2(mode_list):
    length = len(mode_list)
    s_matrix = np.zeros(shape=(length, length))
    for a in range(length):
        for b in range(a):
            s_matrix[a, b] = dtw_distance(process_data(mode_list[a, 1], mode_list[a, 2]).PRESSURE,
                                          process_data(mode_list[b, 1], mode_list[b, 2]).PRESSURE)
            s_matrix[b, a] = s_matrix[a, b]
    s_matrix[np.isnan(s_matrix)] = 999
    return s_matrix


# Spectral Clustering
def spectral_clustering_2(s_matrix, points, k):
    Dn = np.diag(np.power(np.sum(s_matrix, axis=1), -0.5))
    L = np.eye(len(points)) - np.dot(np.dot(Dn, s_matrix), Dn)
    eigvals, eigvecs = LA.eig(L)
    indices = np.argsort(eigvals)[:k]
    k_smallest_eigenvectors = normalize(eigvecs[:, indices])
    #    distance = s_matrix.sum()
    return KMeans(n_clusters=k).fit_predict(k_smallest_eigenvectors)


# Generate daily trend mode for the clusters
def daily_trend_mode_2(k, train, mode_list_1):
    mode_list = []
    for n in range(k):
        k_type = np.array(mode_list_1[:, 2])[np.where(train == n)].tolist()
        mode_list_new = [mode_list_1[:, 1],
                         np.array(k_type)[np.where(similarity_matrix_2(mode_list_1).sum(axis=0).min())].tolist()]
        mode_list = mode_list + mode_list_new
    return mode_list
