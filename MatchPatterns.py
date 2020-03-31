
def get_patterns(clstFilePath, engDictPath, fnameDictPath, pyDictPath):
    lines = open(clstFilePath, "r").read().split('\n')[1:-1]
    resultList = [line.split(',') for line in lines]
    engDict = open(engDictPath, "r").read().lower().split('\n')[:-1]
    fnameDict = open(fnameDictPath, "r").read().lower().split('\n')[:-1]
    pyDict = open(pyDictPath, "r").read().lower().split('\n')[:-1]
    printList, patternList = [], []
    longResultFile = open("ptResult.txt","w")
    longResultFile.write("Each part of every password is matched with a pattern:\n")
    shortResultFile = open("ptShortResult.txt", "w")
    shortResultFile.write("Passwords and their matched patterns are shown as follows:\n")
    for subList in resultList:
        ptSubList = [] # contains passwords, splitting results following by their separate patterns, followed by combined patterns
        shortPtList = [] # contains only passwords and patterns
         # in case of overlap, add all to the pattern result
        overlapStrList = []
        ptSubList.append(subList[0])
        shortPtList.append(subList[0])
        pattern, patternStr = "", ""
        index = 1
        commaProcessed = 0 # if a comma appears in the password, make sure it is correctly processed
        #overlapFound = 0 # if a word is both a family name and a pinyin, add both in the list
        for item in subList[1:]:
            overlapPtList = []
            wordFound = 0 # if found an English word, add the corresponding cluster category after it
            ptSubList.append(item)
            if item.isalpha():
                if item in engDict:
                    if index < len(subList) - 1 and subList[index + 1].startswith("C"):
                        pattern = subList[index + 1]
                        wordFound = 1
                        if item in fnameDict:
                            overlapPtList.append(subList[index + 1])
                            overlapPtList.append("F" + str(len(item)))
                            if item in pyDict:
                                overlapPtList.append("P" + str(len(item)))
                    else:
                        pattern = "L" + str(len(item))
                elif item in fnameDict:
                    pattern = "F" + str(len(item))
                    if item in pyDict:
                        overlapPtList.append("F" + str(len(item)))
                        overlapPtList.append("P" + str(len(item)))
                elif item in pyDict:
                    pattern = "P" + str(len(item))
                else:
                    pattern = "L" + str(len(item))
            else:
                if len(item) == 0:
                    commaProcessed = (commaProcessed + 1) % 2
                    if commaProcessed == 0:
                        pattern = "S1"
                else:
                    if item[0] in "1234567890":
                        pattern = "D" + str(len(item))
                    elif item[0] in "~`!@#$%^&*()_+-=<>,.?/\\{}[]|":
                        pattern = "S" + str(len(item))
                    else:
                        pattern = ""
                        wordFound = 1
            index += 1
            if wordFound == 0:
                ptSubList.append(pattern)
            # dealing with overlaps
            if len(overlapPtList) > 0: # overlap exists for this string
                # there are already multiple pattern strings (more than one overlap)
                if len(overlapStrList) > 0:
                    newStrList = []
                    for overlapStr in overlapStrList:
                        patternStr = overlapStr
                        for overlapPt in overlapPtList:
                            newStr = patternStr + overlapPt
                            newStrList.append(newStr)
                    overlapStrList = newStrList
                else:
                    # first time overlap
                    for overlapPt in overlapPtList:
                        newStr = patternStr + overlapPt
                        overlapStrList.append(newStr)
            else: # no overlap for this string
                # there are already multiple pattern strings
                if len(overlapStrList) > 0:
                    newStrList = []
                    for overlapStr in overlapStrList:
                        newStr = overlapStr + pattern
                        newStrList.append(newStr)
                    overlapStrList = newStrList
                # only one
                else:
                    patternStr += pattern
        if len(overlapStrList) > 0:
            for overlapStr in overlapStrList:
                ptSubList.append(overlapStr)
                shortPtList.append(overlapStr)
                patternList.append(overlapStr)
        else:
            ptSubList.append(patternStr)
            shortPtList.append(patternStr)
            patternList.append(patternStr)

        longResultFile.write(",".join(ptSubList) + "\n")
        shortResultFile.write(",".join(shortPtList) + "\n")
        printList.append(ptSubList)
    return printList, patternList

def get_simple_frequencies(patternList):
    patFreqDict = {}
    for item in patternList:
        key = str(item)
        patFreqDict[key] = patFreqDict.get(key, 0) + 1
    patFreqList = [[key, round(int(value)/len(patternList), 3)] for key, value in patFreqDict.items()]
    patFreqList.sort(key=lambda x:x[1], reverse=True)
    return patFreqList

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

def get_conditional_frequencies(patternList):
    condFreqDict = {}
    pairCount = 0
    for item in patternList:
        subList = split_patterns(item)
        pairCount += (len(subList) - 1)
        for i in range(len(subList) - 1):
            key = str(subList[i]) + "|" + str(subList[i + 1])
            condFreqDict[key] = condFreqDict.get(key, 0) + 1
    condFreqList = [[key, round(int(value)/pairCount, 3)] for key, value in condFreqDict.items()]
    condFreqList.sort(key=lambda x:x[1], reverse=True)
    return condFreqList

def get_pattern_frequencies(resultList, pattern, numToShow):
    patternDict = {}
    patternCount = 0
    for subList in resultList:
        for i in range(1, len(subList) - 2):
            if subList[i + 1] == pattern:
                patternCount += 1
                patternDict[subList[i]] = patternDict.get(subList[i], 0) + 1
    patternList = [[key, round(int(value)/patternCount, 3)] for key, value in patternDict.items()]
    patternList.sort(key=lambda x:x[1], reverse=True)
    return patternList[:numToShow]

def get_all_frequencies(resultList):
    allFreqDict = {}
    f = open("allFrequencies.txt", "w")
    lst1 = [str(a) + str(b) for a in ['D','L'] for b in range(1,9)]
    lst2 = ['S' + str(i) for i in range(1,6)]
    lst = lst1 + lst2
    for pattern in lst:
        f.write("Frequencies for " + pattern + ":\n")
        patternList = get_pattern_frequencies(resultList, pattern, 15)
        allFreqDict[pattern] = patternList
        for subList in patternList:
            f.write(subList[0] + ": " + str(subList[1]) + "\n")
        f.write("\n")
    return allFreqDict

if __name__ == "__main__":
    clstFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Clustering\clstResult.txt"
    engDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\EnglishWords.txt"
    fnameDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\\baijiaxing.txt"
    pyDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\changyongPY.txt"
    resultList, patternList = get_patterns(clstFilePath, engDictPath, fnameDictPath, pyDictPath)
    print(resultList)
    print(patternList)
    patFreqList = get_simple_frequencies(patternList)
    patFreqFile = open("patternFrequencies.txt", "w")
    patFreqFile.write("Patterns and their frequencies in descending order:\n")
    condFreqFile = open("conditionalFrequencies.txt", "w")
    condFreqFile.write("Conditional frequencies for pattern pairs in descending order:\n")
    for subList in patFreqList:
        patFreqFile.write(subList[0] + ": " + str(subList[1]) + "\n")
    condFreqList = get_conditional_frequencies(patternList)
    for subList in condFreqList:
        condFreqFile.write(subList[0] + ": " + str(subList[1]) + "\n")
    allFreqDict = get_all_frequencies(resultList)
    #print(allFreqDict)

