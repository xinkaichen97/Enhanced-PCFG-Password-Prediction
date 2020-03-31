

def test(finalPwdList, pwdFilePath):
    targetPwdList = open(pwdFilePath, "rb").read().split("\\r\\n")[50000:]
    print("Total number of generated passwords: ", len(finalPwdList))
    print("Total number of target passwords: ", len(targetPwdList))
    hitNum = 0
    for pwd in finalPwdList:
        if pwd in targetPwdList:
            hitNum += 1
    print("Matched count: ", hitNum)
    print("Percentage: ", round(hitNum / len(targetPwdList),3))

pwdFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\password dataset\csndpasswd.txt"
resultFilePath ="D:\文档\FUDAN\毕业论文\口令大数据挖掘\GeneratePwd\\final.txt"
lst = open(resultFilePath, "r").read().split(', ')[:100]
print(lst)
