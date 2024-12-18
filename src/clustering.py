from sklearn.cluster import KMeans, DBSCAN

def kmeans_clustering(coords, num_clusters):
    """使用 k-means 聚类"""
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    labels = kmeans.fit_predict(coords)
    return labels, kmeans.cluster_centers_

def dbscan_clustering(coords, eps, min_samples):
    """使用 DBSCAN 聚类"""
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(coords)
    return labels
