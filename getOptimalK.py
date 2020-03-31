from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
def draw_elbow_method4(vectorList):
    bestClstrNum = 0
    scores = []
    K = range(2,30)
    for clstrNum in K:
        clf = KMeans(n_clusters=clstrNum)
        labels = clf.fit_predict(vectorList)
        silhScore = silhouette_score(vectorList, labels)
        scores.append(silhScore)
        scores.append(silhScore)
        if silhScore > maxScore:
            maxScore = silhScore
            bestClstrNum = clstrNum
    plt.plot(K, scores)
    plt.show()
    #return bestClstrNum

def draw_elbow_method(vectorList):
    distortions = []
    K = range(1,30)
    for k in K:
        clf = KMeans(n_clusters=k)
        clf.fit(vectorList)
        distortions.append(sum(np.min(cdist(vectorList,clf.cluster_centers_, 'cosine'),axis=1)))
    #plt.plot(K, distortions)
    #plt.show()
    return distortions

def draw_elbow_method2(vectorList):
    K = range(1,30)
    km = [KMeans(n_clusters=i) for i in K]
    score = [k.fit(vectorList).score(vectorList) for k in km]
    plt.plot(K, score)
    plt.show()

def draw_elbow_method3(vectorList):
    K = range(1,30)
    km = [KMeans(n_clusters=i) for i in K]
    score = [k.fit(vectorList).inertia_ for k in km]
    plt.plot(K, score)
    plt.show()

def optimalK(data, nrefs=5, maxClusters=15):
    gaps = np.zeros((len(range(1, maxClusters)),))
    resultsdf = pd.DataFrame({'clusterCount': [], 'gap': []})
    for gap_index, k in enumerate(range(1, maxClusters)):
        # Holder for reference dispersion results
        refDisps = np.zeros(nrefs)
        # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
        for i in range(nrefs):
            # Create new random reference set
            randomReference = np.random.random_sample(size=len(data))
            # Fit to it
            km = KMeans(k)
            km.fit(randomReference.reshape(-1,1))
            refDisp = km.inertia_
            refDisps[i] = refDisp
        # Fit cluster to original data and create dispersion
        km = KMeans(k)
        km.fit(data)
        origDisp = km.inertia_
        # Calculate gap statistic
        gap = np.log(np.mean(refDisps)) - np.log(origDisp)
        # Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap
        resultsdf = resultsdf.append({'clusterCount': k, 'gap': gap}, ignore_index=True)
    #print(gaps.argmax() + 1, resultsdf)
    return (gaps.argmax() + 1, resultsdf)
 """

def find_elbow_point(vectorList):
    distortions = []
    K = range(1, 30)
    for k in K:
        clf = KMeans(n_clusters=k)
        clf.fit(vectorList)
        distortions.append(sum(np.min(cdist(vectorList, clf.cluster_centers_, 'cosine'), axis=1)))
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
    print(slopes_fwd)
    print(slopes_bwd)
    slopes_diff = [(i + 2, abs(slopes_fwd[i] - slopes_bwd[i])) for i in range(0, length - 4)]
    print(slopes_diff)
    original_diff = slopes_diff
    slopes_diff.sort(key=lambda x:x[1])
    print(slopes_diff)
    return slopes_diff[0][0], original_diff

if __name__ == "__main__":
    splitFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\SplitPassword\\result.txt"
    engDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\EnglishWords.txt"
    resultList, engList = get_english_words(splitFilePath, engDictPath)
    print(resultList)
    print(engList)
    vectorList, foundEngList = get_vector_list(engList)
    distortions = draw_elbow_method(preprocessing.normalize(vectorList))
    print(distortions)
    clusterCount, diff_list = find_elbow_point(distortions)
    # distortions = [6924.053323438027, 6206.972932138832, 5970.891077102066, 5760.592513098514, 5502.034138809513, 5366.971431467169, 5247.179830798364, 5143.146524022225, 5005.589541600542, 4882.218466178387, 4815.366845962925, 4735.99894877305, 4663.026747392168, 4635.643772640808, 4511.915392680141, 4489.520589050345, 4382.899951147456, 4313.726297074952, 4275.2785007389575, 4193.640301923541, 4162.468486859266, 4076.353394366681, 4029.4932326881803, 3967.9872313624733, 3934.807244295044, 3913.7557074491597, 3897.5321543585774, 3822.4615697079507, 3816.081510948158]