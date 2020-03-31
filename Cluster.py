from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
from sklearn import preprocessing
from scipy.spatial.distance import cdist
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt

def get_english_words(splitFilePath, engDictPath):
    f = open(splitFilePath, "r")
    lines = f.read().split('\n')[1:-1]
    fullResultList = [line.split(',') for line in lines]
    engDict = open(engDictPath, "r").read().lower().split('\n')[:-1]
    engList = []
    for subList in fullResultList:
        for item in subList[1:]:
            if item.isalpha():
                if item in engDict and item not in engList:
                    engList.append(item)
    return fullResultList, engList

def get_vector_list(engList):
    model = KeyedVectors.load("word2vec.model")
    vectorList = []
    foundEngList = []
    count = 0
    for item in engList:
        try:
            vectorList.append(model.wv[item])
            foundEngList.append(item)
        except:
            pass
            count += 1
    #vectorList = [model.wv[item] for item in uniqueEngList]
    print(len(engList), count)
    return vectorList, foundEngList

def find_optimal_K(vectorList):
    distortions = []
    K = range(1, 30)
    for k in K:
        clf = KMeans(n_clusters=k)
        clf.fit(vectorList)
        distortions.append(sum(np.min(cdist(vectorList, clf.cluster_centers_, 'cosine'), axis=1)))
    plt.plot(K, distortions,'--ro')
    plt.xlabel("Cluster Number")
    plt.ylabel("Distance")
    plt.show()
    length = len(distortions)
    slopes_fwd, slopes_bwd =[], []
    for i in range(2, length - 2):
        temp_dist = []
        for j in range(i - 2, -1, -1):
            x1 = range(j, i + 1)
            y1 = [distortions[q] for q in range(j, i + 1)]
            k1, b1, r_value, p_value, dist = linregress(x1, y1)
            temp_dist.append((k1, dist))
        temp_dist.sort(key=lambda x:x[1])
        k = temp_dist[0][0]
        slopes_fwd.append(k)
        temp_dist = []
        for p in range(i + 2, length):
            x1 = range(i, p + 1)
            y1 = [distortions[q] for q in range(i, p + 1)]
            k1, b1, r_value, p_value, dist = linregress(x1, y1)
            temp_dist.append((k1, dist))
        temp_dist.sort(key=lambda x:x[1])
        k = temp_dist[0][0]
        slopes_bwd.append(k)
    #print(slopes_fwd)
    #print(slopes_bwd)
    slopes_diff = [(i + 2, abs(slopes_fwd[i] - slopes_bwd[i])) for i in range(0, length - 4)]
    #print(slopes_diff)
    original_diff = slopes_diff
    a = [x[0] for x in slopes_diff]
    b = [x[1] for x in slopes_diff]
    plt.plot(a, b, '--ro')
    plt.xlabel("Cluster Number")
    plt.ylabel("Slope Difference")
    plt.show()
    slopes_diff.sort(key=lambda x:x[1])
    #print(slopes_diff)
    return slopes_diff[0][0], original_diff

def cluster(vectorList, uniqueEngList, clusterCount):
    normVectorList = preprocessing.normalize(vectorList)
    clf = KMeans(n_clusters=clusterCount)
    s = clf.fit(normVectorList)
    labels = clf.labels_
    centers = clf.cluster_centers_
    #print(s)
    #print(labels)
    #print(centers)
    clusterDict = {}
    for i in range(clusterCount):
        clusterDict[i] = []
    for i in range(len(uniqueEngList)):
        if labels[i] in clusterDict.keys():
            clusterDict[labels[i]].append(uniqueEngList[i])
        else:
            clusterDict[labels[i]] = uniqueEngList[i]
    for key in clusterDict:
        clusterDict[key] = list(set(clusterDict[key]))
    return labels, centers, clusterDict

def get_reversed_dict(clusterDict):
    reversedDict = {}
    for key in clusterDict.keys():
        for item in clusterDict[key]:
            reversedDict[item] = key
    return reversedDict

def get_cluster_info(resultList, engList, clusterDict):
    clstResultList = []
    reversedDict = get_reversed_dict(clusterDict)
    for subList in resultList:
        clstSubList = []
        clstSubList.append(subList[0])
        for item in subList[1:]:
            clstSubList.append(item)
            if item.isalpha():
                if item in engList:
                    clstSubList.append("C" + str(reversedDict[item]))
        clstResultList.append(clstSubList)
    #print(clstResultList)
    f = open("clstResult.txt", "w")
    f.write("Each English word in the splitting results is followed by its cluster number:\n")
    for subList in clstResultList:
        f.write(",".join(subList) + "\n")
    return clstResultList

if __name__ == "__main__":
    """
    diff = [(25, 32.011865010570546), (13, 47.17774661960834), (26, 119.27565806542896), (23, 305.3652556004182),
     (24, 349.1851891588284), (21, 356.1696701665718), (20, 384.64119508501904), (19, 394.69584365747494),
     (18, 418.9154507892623), (16, 494.58044582540083), (22, 511.28558976555394), (17, 525.1304363061748),
     (14, 773.534605997475), (15, 779.854972943241), (12, 1028.7193854472978), (11, 1174.1574083239748),
     (5, 1277.0652640683563), (8, 1373.985048024319), (10, 1423.1372586927416), (9, 1465.386232999201),
     (7, 1768.269293871609), (6, 1867.6102042454324), (4, 2034.299081179703), (3, 2245.1754529332325),
     (2, 7023.371665748225)]
    diff.sort(key=lambda x:x[0])
    print(diff)
    k = [x[0] for x in diff]
    dist = [x[1] for x in diff]
    plt.plot(k, dist, '--bo')
    plt.xlabel("Cluster Number")
    plt.ylabel("Slope Difference")
    plt.title('Slope Difference for Each Cluster Number')
    plt.show()"""
    splitFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\SplitPassword\\result.txt"
    #splitFilePath = "H:\cluster\\result.txt"
    engDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\EnglishWords.txt"
    #engDictPath = "H:\dictionaries\EnglishWords.txt"
    engList = open(engDictPath, "r").read().lower().split('\n')[:-1]
    resultList, engList = get_english_words(splitFilePath, engDictPath)
    #print(resultList)
    #print(engList)

    vectorList, foundEngList = get_vector_list(engList)
    clusterCount, diffList = find_optimal_K(vectorList)
    print(clusterCount)
    f = open("log.txt", "w")
    f.write(str(clusterCount)+'\n')
    f.write(str(diffList))
    #clusterCount"""

    print('Starting to cluster...')
    #clusterCount = 19
    clusterDict = cluster(vectorList, foundEngList, clusterCount)[2]
    print(clusterDict)
    f = open("clusterDict.txt", "w")
    f.write(str(clusterDict))
    clstResultList = get_cluster_info(resultList, foundEngList, clusterDict)


