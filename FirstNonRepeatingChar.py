import json


def firstNonRepeating(string):
    emptyDict = {}
    for element in range(1, len(string)):
        ele = string[element]
        if ele in emptyDict:
            emptyDict[ele] = emptyDict.get(ele)+1
        else:
            emptyDict[ele] = 1
    print(emptyDict)
    for element in range(1, len(string)):
        ele = string[element]
        if (emptyDict.get(ele)) == 1:
            return string.index(ele)
    return  -1
a = firstNonRepeating(('hackthegame'))
print(a)





