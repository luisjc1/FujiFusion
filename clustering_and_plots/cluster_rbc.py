import matplotlib
matplotlib.use('Agg')
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle
import statistics

def load_data(filename):
    data = pd.read_csv(filename)
    return data 

def cluster(data):
    tickers = data.loc[:, "Tickers"]
    subset = data.loc[:, "Debt/EBITDA":"EBITDA/Total assets etc"]
    test = data.loc[:,"L_term_numrating"].values.reshape(-1,1)
    
    kmeans = KMeans(n_clusters=12, precompute_distances='auto', algorithm='auto')
    kmeans.fit(subset)
    clusters = kmeans.labels_.tolist()
    
    output = data.loc[:, "date":"L_term_numrating"]
    output["cluster"] = clusters
    output.set_index("cluster")
    print(output)
    return output
    #print(cluster['cluster'].value_counts())


def meanshift(data):
    tickers = data.loc[:, "Tickers"]
    subset = data.loc[:, "Debt/EBITDA":"EBITDA/Total assets etc"]
    test = data.loc[:,"L_term_numrating"].values.reshape(-1,1)
   
    bandwidth = estimate_bandwidth(subset)
    means = MeanShift(bandwidth=bandwidth)
    means.fit(subset)
    clusters = means.labels_.tolist()
    cluster_centers = means.cluster_centers_

    labels_unique = np.unique(clusters)
    n_clusters_ = len(labels_unique)

    '''
    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = clusters == k
        cluster_center = cluster_centers[k]
        plt.plot(subset[my_members, 0], subset[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                                             markeredgecolor='k', markersize=14)
        plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    '''
    output = data.loc[:, "date":"L_term_numrating"]
    output["cluster"] = clusters
    output.set_index("cluster")
    return output
    print(output)

def cluster_stats(output):
    for i in range(12):
        print("==========================================================")
        correct_num = output.loc[output['L_term_numrating'] == i].shape[0]
        print(correct_num)
        cluster_comps = output.loc[output['cluster'] == i]
        print("points in cluster", i, "=", cluster_comps.shape[0])
        try:
            print("mean of cluster", i, "=", statistics.mean(cluster_comps.loc[:,"L_term_numrating"].tolist()))
        except:
            continue
        try:
            print("stdv of cluster", i, "=", statistics.stdev(cluster_comps.loc[:,"L_term_numrating"].tolist()))
        except:
            continue

data = load_data("features_ratings.csv")
op = cluster(data)
cluster_stats(op)
op2 = meanshift(data)
cluster_stats(op2)
