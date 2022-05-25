import sys
import os
import time
from pathlib import Path

import numpy as np
import skimage
from sklearn.decomposition import PCA
from sklearn.random_projection import GaussianRandomProjection
from sklearn.cluster import KMeans


def calc_error(X, label_lst, k):
    
    # Calculate cluster centers
    cluster_center_lst = np.empty((k, X.shape[1]))
    
    for i in range(k):
        cluster_center_lst[i] = np.mean(X[label_lst == i])
    
    error = np.linalg.norm(X - cluster_center_lst[label_lst], axis=1).mean()
    return error

if __name__ == '__main__':

    dataset = sys.argv[1]
    width = int(sys.argv[2])
    d_pca = int(sys.argv[3])
    k = int(sys.argv[4])

    height = width
    folder_path = f'{dataset}_{width}'
    filename_lst = os.listdir(folder_path)
    n_img = len(filename_lst)
    result_filepath = Path('result') / f'{dataset}_{width}_{d_pca}_{k}.csv'

    # Read the images
    X = np.empty((n_img, width * height * 3), dtype=np.uint8)
    for i, filename in enumerate(filename_lst):
        input_filepath = Path(folder_path) / filename
        im = skimage.io.imread(input_filepath)

        if im.ndim != 3:
            im = np.stack((im,)*3, axis=-1)

        im = im.flatten()
        X[i] = im
    
    # Clustering using PCA
    t_start = time.perf_counter()

    # Reduce dimensions
    mdl = PCA(n_components=d_pca)
    X_tr = mdl.fit_transform(X)

    # Cluster
    mdl = KMeans(n_clusters=k)
    mdl.fit(X_tr)

    t_end = time.perf_counter()

    pca_elapsed = t_end - t_start
    pca_error = calc_error(X, mdl.labels_, k)

    if not os.path.isdir('result'):
        os.mkdir('result')
    with open(result_filepath, 'w') as file:
        file.write(f'PCA,{pca_elapsed},{pca_error}\n')

    # Clustering using Random Projection

    n_component_lst = [100, 200, 400, 800, 1000, 2000, 4000]
    elapsed_lst = []
    error_lst = []

    for n_component in n_component_lst:
        
        t_start = time.perf_counter()
        
        # Reduce dimensions
        mdl = GaussianRandomProjection(n_components=n_component)
        X_tr = mdl.fit_transform(X)
        
        # Cluster
        mdl = KMeans(n_clusters=k)
        mdl.fit(X_tr)
        
        t_end = time.perf_counter()
        elapsed = t_end - t_start
        error = calc_error(X, mdl.labels_, k)
        
        elapsed_lst.append(elapsed)
        error_lst.append(error)
    
    with open(result_filepath, 'a') as file:
        for n, elapsed, error in zip(n_component_lst, elapsed_lst, error_lst):
            file.write(f'{n},{elapsed},{error}\n')