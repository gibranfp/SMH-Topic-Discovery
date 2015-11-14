import numpy as np
import smh.smh_api as sa
from sklearn.utils.linear_assignment_ import linear_assignment

def topics_intra_distance(topics):
    distmat = np.zeros((topics.size(), topics.size()))
    for i, t1 in enumerate(topics.ldb):
        for j, t2 in enumerate(topics.ldb):
            distmat[i, j] = 1.0 - sa.list_jaccard(t1, t2)
        
    return distmat

def topics_inter_distance(topics1, topics2):
    distmat = np.zeros((topics1.size(), topics2.size()))
    for i, t1 in enumerate(topics1.ldb):
        for j, t2 in enumerate(topics2.ldb):
            distmat[i, j] = 1.0 - sa.list_jaccard(t1, t2)
        
    return distmat

def topics_entropy(distmat):
    np.fill_diagonal(distmat, 1.0)
    
    return -np.sum(mean_dist * np.log(mean_dist))

def topics_mean_intra_distance(topics):
    distmat = topics_intra_distance(topics)

    return np.sum(distmat, axis=1) / (distmat.shape[1] - 1)

def topics_min_intra_distance(topics):
    distmat = topics_intra_distance(topics)
    np.fill_diagonal(distmat, 1.0)
    
    return np.argmin(dist, axis=1), np.min(dist, axis=1)

def topics_entropy_mean_dist(topics):
    mean_dist = topics_mean_intra_distance(topics)
    
    return -np.sum(mean_dist * np.log(mean_dist))

def topics_mean_entropy(topics):
    distmat = topics_intra_distance(topics)
    np.fill_diagonal(distmat, 1.0)
    
    return (-np.sum(distmat * np.log(distmat), axis=1)) / (distmat.shape[1] - 1)

def topics_entropy_sum(topics):
    distmat = topics_intra_distance(topics)
    np.fill_diagonal(distmat, 1.0)
    
    return -np.sum(distmat * np.log(distmat), axis=1)

def topics_mean_inter_distance(topics1, topics2):
    distmat = topics_inter_distance(topics1, topics2)

    return np.mean(distmat, axis=1)

def topics_min_inter_distance(topics1, topics2):
    distmat = topics_inter_distance(topics1, topics2)

    return np.argmin(distmat, axis=1), np.min(distmat, axis=1)

def topics_consistency(topics1, topics2, thres=0.8):
    distmat = topics_inter_distance(topics1, topics2)
    distmat[distmat > thres] = np.inf
    
    indices = linear_assignment(distmat)
    
    not_in_topics1 = np.delete(np.arange(topics1.size()), indices[:, 0])
    not_in_topics2 = np.delete(np.arange(topics2.size()), indices[:, 1])

    return not_in_topics1, not_in_topics2, indices, distmat[indices[:, 0], indices[:, 1]]

def topics_in_docs(topics, docs, thres=0.6):
    indocs = np.zeros((docs.size(), topics.size()), dtype=bool)
    
    for i, d in enumerate(docs.ldb):
        for j, t in enumerate(topics.ldb):
            if sa.list_overlap(d,t) > thres:
                indocs[i,j] = True
                
    return indocs
