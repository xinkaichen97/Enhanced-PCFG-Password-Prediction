import re

def get_pinyin_count(pwdFilePath, fnameDictPath, pyPath):
    pwdList = open(pwdFilePath, "r").read().lower().split('\n')[:-1]
    fnameDict = open(fnameDictPath, "r").read().lower().split('\n')[:-1]

def get_pwd_list(pwdFilePath, engDictPath):
    #pwdFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\数据集\password dataset\csndpasswd.txt"

    txtStr = open(pwdFilePath, "rb").read()
    txtStr = str(txtStr)[2:-1]
    pwdList = txtStr.split("\\r\\n")
    #print(pwdList[:10])
    #print(ptt)
    #pwdList = open(pwdFilePath, "r").read().lower().split('\n')[:-1]
    print(len(pwdList))
    alpha_count = 0
    eng_count = 0
    engDict = open(engDictPath, "r").read().lower().split('\n')[:-1]
    print("Passwords read.")
    uniquePwdList = []
    for pwd in pwdList:
        for word in engDict:
           if pwd.lower().find(word) >= 0:
               uniquePwdList.append(pwd)
               break
    """if re.search('[a-zA-Z]', pwd):
        alpha_count += 1
        #uniquePwdList.append(pwd)
        for word in engDict:
            if pwd.lower().find(word) >= 0:
                eng_count += 1
                uniquePwdList.append(pwd)
                break
    print(alpha_count, eng_count)"""
    return uniquePwdList

pwdFilePath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\password dataset\\renrenpasswd.txt"
engDictPath = "D:\文档\FUDAN\毕业论文\口令大数据挖掘\Data\dictionaries\EnglishWords.txt"
#pwdFilePath = 'D:\文档\FUDAN\毕业论文\口令大数据挖掘\SplitPassword\\result.txt'
#engDictPath = 'H:\splitpwd\EnglishWords.txt'
pwdList = get_pwd_list(pwdFilePath, engDictPath)
print(len(pwdList))
f = open('renren_eng.txt', 'w')
for pwd in pwdList:
    f.write(pwd + '\n')

