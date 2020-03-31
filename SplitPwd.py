from os import listdir
from os.path import isfile, join
import re

def combine_dictionaries(dictPath):
    #dictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\数据集\dictionaries"
    dictList = [f for f in listdir(dictPath) if isfile(join(dictPath, f))]
    combinedDict = []
    for dic in dictList:
        dicFile = open(join(dictPath, dic), "r")
        combinedDict += dicFile.read().lower().split()
    return combinedDict

def get_pwd_list(pwdFilePath, pwdCount):
    #pwdFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\数据集\password dataset\csndpasswd.txt"
    txtFile = open(pwdFilePath, "rb")
    txtStr = txtFile.read()
    txtStr = str(txtStr)[2:-1]
    pwdList = txtStr.split("\\r\\n")[:pwdCount]
    print("Passwords read.")
    uniquePwdList = []
    for pwd in pwdList:
        if re.search('[a-zA-Z]', pwd):
            uniquePwdList.append(pwd)
    return uniquePwdList

def get_type(char):
    if char in "1234567890":
        return "number"
    elif char.lower() in "abcdefghijklmnopqrstuvwxyz":
        return "alpha"
    elif char in "~`!@#$%^&*()_+-=<>,.?/\\{}[]|":
        return "special"
    else:
        return "others"

def split_different_types(pwdStr):
    resultList = []
    tempStr = pwdStr[0]
    for s in pwdStr[1:]:
        if get_type(s) == get_type(tempStr[-1]):
            tempStr += s
        else:
            resultList.append(tempStr)
            tempStr = s
    resultList.append(tempStr)
    return resultList

def get_max_len(lst):
    maxLen = 0
    for subList in lst:
        length = 0
        for item in subList:
            length += len(item)
        if length > maxLen:
            maxLen = length
    return maxLen

def get_min_num(lst, maxLen):
    minNum = max(len(subList) for subList in lst)
    for subList in lst:
        length = 0
        for item in subList:
            length += len(item)
        if length >= maxLen:
            if minNum > len(subList):
                minNum = len(subList)
    return minNum

def get_result(lst, maxLen, minNum):
    newList = []
    for subList in lst:
        length = 0
        for item in subList:
            length += len(item)
        if length == maxLen and len(subList) == minNum:
             newList.append(subList)
    uniqueList = []
    count = 0
    uniqueList.append(newList[0])
    for subList in newList:
        for item in subList:
            if item in uniqueList[0]:
                count += 1
        if count < len(uniqueList[0]):
            uniqueList.append(subList)
    if len(uniqueList) > 1:
        return "Ambiguous results: " + str(uniqueList)
    else:
        return uniqueList[0]

def split_alpha(pwdStr, dict):
    smallDict = [s for s in dict if s in pwdStr]
    if len(smallDict) == 0:
        singleList = []
        singleList.append(pwdStr)
        return singleList
    smallDict = sorted(smallDict, key=len, reverse=True)
    resultList = []
    tempStr = pwdStr
    for entry in smallDict:
        pwdStr = tempStr
        tempList = []
        tempList.append(entry)
        pwdStr = pwdStr.replace(entry,"|")
        for item in smallDict:
            if item in pwdStr:
                tempList.append(item)
                pwdStr = pwdStr.replace(item, "|")
        #remainingStr = pwdStr.rstrip("|").lstrip("|")
        #remainList = re.split(r"[^a-zA-Z0-9\s]", remainingStr)
        #for rmResult in remainList:
        #    if len(rmResult) > 0:
        #        tempList.append(rmResult)
        resultList.append(tempList)
    maxLen = get_max_len(resultList)
    minNum = get_min_num(resultList, maxLen)
    print(maxLen, minNum, resultList)
    finalResult = get_result(resultList, maxLen, minNum)
    finalResult.sort(key=lambda x:tempStr.find(x))
    print(finalResult)
    return finalResult

def get_final_results(pwdFilePath, pwdNum, dictFilePath, engDictPath):
    pwdList = get_pwd_list(pwdFilePath, pwdNum)
    print(len(pwdList))
    splitList = [split_different_types(pwdStr.lower()) for pwdStr in pwdList]
    combinedDict = combine_dictionaries(dictFilePath)
    engDict = open(engDictPath, "r").read().lower().split('\n')[:-1]
    finalList = []
    index = 0
    print("Starting to split...")
    for subList in splitList:
        finalSubList = []
        engCount = 0
        for item in subList:
            if item.isalpha():
                alphaList = split_alpha(item, combinedDict)
                for result in alphaList:
                    if result in engDict:
                        engCount += 1
                if len(alphaList) == 1 and len(alphaList[0]) == len(item): # only one result
                    finalSubList.append(alphaList[0])
                    continue
                else:
                    for result in alphaList:
                        finalSubList.append(result)
            else:
                finalSubList.append(item)
        #finalSubList.sort(key=lambda x:pwdList[index].find(x))
        #if engCount == 0:
        #    continue
        tempList = []
        tempList.append(pwdList[index])
        finalSubList = tempList + finalSubList
        index += 1
        if engCount > 0:
            finalList.append(finalSubList)
    f = open("result.txt", "w")
    f.write("Original passwords following by splitting results:\n")
    print(len(finalList))
    for subList in finalList:
        f.write(",".join(subList) + "\n")
    return finalList

if __name__ == "__main__":
    #pwdFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\password dataset\csdnpasswd_eng.txt"
    pwdFilePath = 'H:\splitpwd\csdnpasswd_eng.txt'
    #engDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\EnglishWords.txt"
    engDictPath = 'H:\splitpwd\dictionaries\EnglishWords.txt'
    pwdNum = 255078
    #dictFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries"
    dictFilePath = 'H:\splitpwd\dictionaries'
    diction = combine_dictionaries('D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries')
    #print(len(diction))
    split_alpha('chenlovegu1997', diction)
    #finalList = get_final_results(pwdFilePath, pwdNum, dictFilePath, engDictPath)

    #print(finalList)
    """
    dictFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries"
    combinedDict = combine_dictionaries(dictFilePath)
    print(split_alpha("syhopen", combinedDict))"""
