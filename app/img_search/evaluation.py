import os
import random as rd
import time

import numpy as np
from progressbar import *

from config import *
from .LSH import *
from .utils import *
from .img_loader import *


def build_index():
    if not os.path.exists('img_infos.npy'):
        img_list = []
        widgets = ['Creating index: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA()]
        np_list = os.listdir('np/')
        total = len(np_list)
        pbar = ProgressBar(widgets=widgets, maxval=10*total).start()
        for i, feature in enumerate(np_list):
            feature_path = os.path.join('np/', feature)
            feature_vector = np.load(feature_path).flatten()
            img_list.append((feature_vector, feature.split('_')[0]))
            pbar.update(10 * i + 1)
        pbar.finish()
        img_list = np.vstack(img_list)
        np.save('img_infos.npy', img_list)
        return img_list
    img_list = np.load('img_infos.npy', allow_pickle=True)
    return img_list


def build_LSH_index(lsh):
    if not os.path.exists('LSH_index.npy'):
        widgets = ['Creating LSH index: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA()]
        np_list = os.listdir('np/')
        total = len(np_list)
        pbar = ProgressBar(widgets=widgets, maxval=10*total).start()
        for i, feature in enumerate(np_list):
            feature_path = os.path.join('np/', feature)
            feature_vector = np.load(feature_path).flatten()
            lsh.index(feature_vector, feature.split('_')[0])
            pbar.update(10 * i + 1)
        pbar.finish()
        lsh.save()
        return lsh
    lsh.load()
    return lsh

def get_index():
    return np.load(os.path.join(os.getcwd(), 'app', 'img_search', 'img_infos.npy'), allow_pickle=True)

def get_lsh_index(lsh):
    lsh.load()
    return lsh


def lsh_search(lsh, query_vector, MAX_QUERY_NUM):
    start = time.time()
    dist_list = lsh.query(query_vector, MAX_QUERY_NUM)
    end = time.time()
    res = [int(item[0][1]) for item in dist_list[:MAX_QUERY_NUM]]
    end = time.time()
    print('Time for LSH searchings: {:.5f}'.format(end - start))
    print(res[:500])
    return res


def KNN_search(index, query_vector, MAX_QUERY_NUM):
    start = time.time()
    dist_list = []
    widgets = ['Calculating distance: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA()]
    total = len(index)
    pbar = ProgressBar(widgets=widgets, maxval=10*total).start()
    for i, f in enumerate(index):
        dist = square_dist(f[0], query_vector)
        dist_list.append((dist, f[1]))
        pbar.update(10 * i + 1)
    pbar.finish()
    dist_list.sort(key=lambda x: x[0])
    res = [int(item[1]) for item in dist_list[:MAX_QUERY_NUM]]
    end = time.time()
    print('Time for KNN searchings: {:.5f}'.format(end - start))
    print(res[:500])
    return res


def query(query_img_path):
    data = DataLoader(MODEL_NAME)
    query_embed = data.extract_single_img_embed(query_img_path).flatten()
    if SEARCH_METHOD == 0:
        index = get_index()
        return KNN_search(index, query_embed, MAX_QUERY_NUM)
    else:
        lsh = LSH(100, 2048, hash_function='dot')
        lsh = get_lsh_index(lsh)
        return lsh_search(lsh, query_embed, MAX_QUERY_NUM)



if __name__ == "__main__":
    query('data/image/400848331_0.jpg')