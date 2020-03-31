import heapq
from queue import PriorityQueue
import MatchPatterns
import itertools
import random
import datetime

class PreTerminal:
    def __init__(self, structure="", baseStr="", pivotValue=0, numStrings=0, probability=0.0):
        self.structure = structure
        self.baseStr = baseStr
        self.pivotValue = pivotValue
        self.numStrings = numStrings
        self.probability = probability

def get_dictionaries(patFreqPath, strFreqPath):
    lines = open(patFreqPath, "r").read().split('\n')[1:-1]
    patternList = [line.split(': ') for line in lines]
    lines = open(strFreqPath, "r").read().split('\n')[1:-1]
    allFreqDict = {}
    pattern = ""
    for line in lines:
        if line.startswith("Frequencies"):
            pattern= line.split()[-1].lstrip()
            allFreqDict[pattern] = []
        elif len(line) == 0:
            continue
        else:
            lst = line.split(':')
            allFreqDict[pattern].append(lst)
    return patternList, allFreqDict

def split_patterns(patternStr):
    patternList = []
    start, end = 0, 0
    for i in range(1, len(patternStr)):
        if patternStr[i] in ['D','F','C','L','S','P']:
            end = i
            patternList.append(patternStr[start:end])
            start = i
    patternList.append(patternStr[end:])
    return patternList

def fill_init_values(baseStr, freqDict):
    returnStr = ""
    baseStrList = split_patterns(baseStr)
    for bStr in baseStrList:
        if bStr[0] in ['D','L','S']:
            returnStr += freqDict[bStr][0][0]
        else:
            returnStr += bStr
    return returnStr

def split_types(baseStr, structure):
    strList = []
    baseList = split_patterns(baseStr)
    for base in baseList:
        if base[0] in ['L','S','D']:
            strLen = int(base[1:])
            strList.append(structure[:strLen])
            structure = structure[strLen:]
        elif base[0] in ['C','F','P']:
            strList.append(base)
            structure = structure[len(base):]
            #print(structure)
    return strList

def fill_words(structure, baseStr, pfcDict):
    ptList = split_types(baseStr, structure)
    allList = []
    for pt in ptList:
        if pt[0] in ['F','P','C']:
            allList.append(pfcDict[pt])
        else:
            lst = [pt]
            allList.append(lst)
    #print(allList)
    combinedList = list(itertools.product(*allList))
    strList = ["".join(lst) for lst in combinedList]
    #print(strList)
    return strList

def get_final_pwd(newPwdList, pfcDict):
    print("Starting to get final passwords...")
    #t1 = datetime.datetime.now()
    finalPwdList = []
    f = open('LongPattern.txt', 'w')
    count = 0
    for pwdStr, baseStr in newPwdList:
        count += 1
        if get_pattern_num(pwdStr) > 4:
            f.write(pwdStr + '\n')
            print('Too long:', pwdStr)
            continue
        try:
            finalPwdList += fill_words(pwdStr, baseStr, pfcDict)
            print(count)
            #if count > 10000:
            #    if (datetime.datetime.now() - t1).total_seconds() > 21600: # set the execution time limit as 6 hours
            #        return finalPwdList
        except:
            pass
    return finalPwdList

def get_probability(baseStr, ptStructure, patternDict, freqDict):
    p = patternDict[baseStr]
    ptList = split_patterns(baseStr)
    strList = split_types(baseStr, ptStructure)
    for i in range(len(strList)):
        #print(strList)
        if strList[i][0] in ['C','F','P']:
            continue
        for lst in freqDict[ptList[i]]:
            if lst[0] == strList[i]:
                p *= lst[1]
    return -p

def get_pattern_num(patternStr):
    ptNum = 0
    for i in range(0, len(patternStr)):
        if patternStr[i] in ['D','L','S','F','P','C']:
            ptNum += 1
    return ptNum

def decrement(baseStr, structure, freqDict, i):
    #print(structure)
    strList = split_types(baseStr, structure)
    #print(strList)
    tempStr = strList[i]
    if tempStr[0] in ['F', 'P', 'C']:
        return structure
    oldStr = tempStr
    newStr = ""
    lst = freqDict[split_patterns(baseStr)[i]]
    for j in range(len(lst)):
        if lst[j][0] == oldStr:
            if j == len(lst) - 1:
                newStr = oldStr
            else:
                newStr = lst[j + 1][0]
    returnStr = ""
    for k in range(len(strList)):
        if k == i:
            returnStr += newStr
        else:
            returnStr += strList[k]
    #structure = structure.replace(oldStr, newStr)
    return returnStr

def generate_pwd(patFreqList, freqDict):
    f = open("log.txt", "w")
    newPwdList = []
    queue = PriorityQueue()
    patternDict = {}
    patFreqList = patFreqList[:1200]
    for subList in patFreqList:
        patternDict[subList[0]] = subList[1]
    baseStrList = [pat[0] for pat in patFreqList]
    for baseStr in baseStrList:
        if len(baseStr) > 10:
            if get_pattern_num(baseStr) > 5:
                continue
        workingValue = PreTerminal()
        workingValue.baseStr = baseStr
        workingValue.structure = fill_init_values(baseStr, freqDict)
        newPwdList.append((workingValue.structure, workingValue.baseStr))
        if workingValue.structure == baseStr:
            workingValue = PreTerminal()
            continue
        workingValue.probability = get_probability(baseStr, workingValue.structure, patternDict, freqDict)
        f.write(workingValue.structure + ", ")
        f.write(str(workingValue.probability * 10000) + "\n")
        workingValue.pivotValue = 0
        workingValue.numStrings = get_pattern_num(baseStr)
        #heapq.heappush(queue, (workingValue.probability * 10000, workingValue))
        queue.put((workingValue.probability * 10000, workingValue.structure, workingValue.baseStr, workingValue.pivotValue, workingValue.numStrings))
    #for item in queue:
    #    f.write(str(item[1].probability) + "," + item[1].structure + ", ")
    #f.write("\n")
    #workingValue = heapq.heappop(queue)[1]
    prob, struct, bStr, pValue, numStr = queue.get()
    workingValue = PreTerminal(struct, bStr, pValue, numStr, prob)
    print(workingValue.structure)
    f.write("Working: " + workingValue.structure + "\n")
    while workingValue is not None:
        if queue.empty():
            count = 0
            for j in range(workingValue.pivotValue, workingValue.numStrings):
                insertValue = PreTerminal()
                insertValue.structure = decrement(workingValue.baseStr, workingValue.structure, freqDict, j)
                if insertValue.structure == workingValue.structure:
                    count += 1
            if count == (workingValue.numStrings - workingValue.pivotValue):
                break
        for i in range(workingValue.pivotValue, workingValue.numStrings):
            insertValue = PreTerminal()
            insertValue.structure = decrement(workingValue.baseStr, workingValue.structure, freqDict, i)
            if insertValue is not None and insertValue.structure != workingValue.structure:
                insertValue.baseStr = workingValue.baseStr
                insertValue.probability = get_probability(insertValue.baseStr, insertValue.structure, patternDict, freqDict)
                insertValue.pivotValue = i
                insertValue.numStrings= workingValue.numStrings
                #heapq.heappush(queue, (insertValue.probability * 10000, insertValue))
                queue.put((insertValue.probability * 10000, insertValue.structure, insertValue.baseStr, insertValue.pivotValue, insertValue.numStrings))
                f.write("Inserting: " + insertValue.structure + "\n")
                print(insertValue.structure)
        #workingValue = heapq.heappop(queue)[1]
        prob, struct, bStr, pValue, numStr = queue.get()
        workingValue = PreTerminal(struct, bStr, pValue, numStr, prob)
        f.write("Working: " + workingValue.structure + "\n")
        #f.write(workingValue.baseStr + str(workingValue.structure) + str(workingValue.pivotValue) + str(workingValue.numStrings))
        #print("Len: ",len(queue))
        newPwdList.append((workingValue.structure, workingValue.baseStr))
    return newPwdList

def test(finalPwdList, pwdFilePath):
    print("Starting to test...")
    txtStr = open(pwdFilePath, "rb").read()
    txtStr = str(txtStr)[2:-1]
    targetPwdList = txtStr.split("\\r\\n")[255078:]
    f = open('HitRate.txt', 'w')
    print("Total number of generated passwords: ", len(finalPwdList))
    f.write('Total number of generated passwords: ' + str(len(finalPwdList)) + '\n')
    print("Total number of target passwords: ", len(targetPwdList))
    f.write('Total number of target passwords: ' + str(len(targetPwdList)) + '\n')
    hitNum = 0
    #i = int(len(finalPwdList) / 20)
    #finalPwdSet = set(finalPwdList)
    #targetSet = set(targetPwdList)
    index = 0
    for pwd in targetPwdList:
        index += 1
        if index % 10000 == 0:
            print(index)
        if pwd in finalPwdList:
            hitNum += 1
    print("Matched count: ", hitNum)
    f.write('Matched count: ' + str(hitNum) + '\n')
    print("Percentage: ", round(hitNum / len(targetPwdList), 3))
    f.write('Percentage: ' + str(round(hitNum / len(targetPwdList), 3)) + '\n')

if __name__ == "__main__":
    """
    pwdFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\password dataset\csdnpasswd_eng.txt"
    clstFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Clustering\clstResult.txt"
    engDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\EnglishWords.txt"
    fnameDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\\baijiaxing.txt"
    pyDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\changyongPY.txt"
    """
    #pwdFilePath = "H:\exe\csndpasswd.txt"
    pwdFilePath = "H:\csdnpasswd_eng.txt"
    clstFilePath = "H:\clstResult.txt"
    engDictPath = "H:\dictionaries\EnglishWords.txt"
    fnameDictPath = "H:\dictionaries\\baijiaxing.txt"
    pyDictPath = "H:\dictionaries\changyongPY.txt"
    resultList, patternList, pfcDict = MatchPatterns.get_patterns(clstFilePath, engDictPath, fnameDictPath, pyDictPath)
    print(pfcDict)
    #f = open('pfcDict.txt', 'w')
    #f.write(str(pfcDict))
    #fill_words("F3$$C7123", "F3S2C7D3", pfcDict)

    patFreqList = MatchPatterns.get_simple_frequencies(patternList)
    #f = open('patternFrequency.txt', 'w')
    #f.write(str(patFreqList))
    allFreqDict = MatchPatterns.get_all_frequencies(resultList)
    #f = open('allFrequency.txt', 'w')
    #f.write(str(allFreqDict))
    #print(patFreqList)
    #print(allFreqDict)

    newPwdList = generate_pwd(patFreqList, allFreqDict)
    f = open('Len.txt', 'w')
    f.write(str(len(newPwdList)))
    #f = open('newPwdList.txt', 'w')
    #f.write(str(newPwdList))
    #f.write('\n'+str(len(newPwdList)))
    #print(ptt)
    #print(newPwdList)
    finalPwdList = get_final_pwd(newPwdList[:10000], pfcDict)
    print('Final password generation finished.')
    #f = open("final.txt", "w")
    #f.write(str(finalPwdList))
    #f.write(", ".join(finalPwdList))
    #print(finalPwdList)
    #print(len(finalPwdList))
    test(finalPwdList, pwdFilePath)