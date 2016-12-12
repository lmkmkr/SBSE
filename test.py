#-*- coding: utf-8 -*-

from datetime import datetime
import random
import math
import sys


##makefile list with lexicographical order
def constructFileList(commits):
    fileList = set()
    fileList.add("root")
    for commit in commits:
        for files in commit[2]:
            path = files.split("/")
            file = "root"
            fileList.add(file)
            for name in path:
                file += "/"+name
                fileList.add(file)
    ret = list(fileList)
    ret.sort()
    return ret

def constructDictionary(flist):
    dictionary = dict()
    for i in range(len(flist)):
        dictionary[flist[i]] = i
    return dictionary

def constructFileNameList(flist):
    fileNameList = list()
    fileNameList.append("root")
    for i in range(1,len(flist)):
        filename = flist[i][flist[i].rindex("/")+1:]
        fileNameList.append(filename)
    return fileNameList



def constructFileSystem(flist):
    fsystem = [[-1]]
    for i in range(1,len(flist)):
        parentfile = flist[i][:flist[i].rindex("/")]
        parPosit = flist.index(parentfile)
        fsystem[parPosit].append(i)
        fsystem.append([parPosit])
    return fsystem

def totRank(history,fsystem,fnlist,rankFunc = None, putFirstChar = False):
    frequency = None
    fileExist = [False]*len(fsystem)
    fileExist[0] = True
    if (rankFunc == 1) | (rankFunc == 2):
        frequency = [0]*len(fsystem)
    totRank = 0
    totTry = 0
    totOne = 0
    for log in history:
        route = []
        idx = log
        while idx != -1:
            route.insert(0,idx)
            if not fileExist[idx]:
                fileExist[idx] = True
            idx = fsystem[idx][0]
        for i in range(0,len(route)-1):
            sidx = route[i]
            didx = route[i+1]
            Files = list(filter(lambda x,fe = fileExist: fe[x],fsystem[sidx][1:]))
            if putFirstChar :
                firstchar = fnlist[didx][0]
                Files = list(filter(lambda x,fn = fnlist,char = firstchar: (fnlist[x][0] == char),Files))
            if len(Files) <= 1:
                totOne += 1
            sortedFiles = []
            if rankFunc is None:
                sortedFiles = Files
            elif rankFunc == 1:
                sortedFiles = frequencyRanking(Files,fsystem,frequency)
                frequency[didx] += 1
            elif rankFunc == 2:
                sortedFiles = antLikeRanking(Files,fsystem,frequency)
                frequency[didx] += 10
            totTry += 1
            if rankFunc == 4 :
                totRank += len(Files)
            else:
                totRank += sortedFiles.index(didx)+1
    if (rankFunc == 1) | (rankFunc == 2):
        frequency.sort(reverse=True)
        print(frequency[0]," ",frequency[1]," ",frequency[2]," ",frequency[3]," ",frequency[4])
    return (totTry,totRank,totOne)
                
def constructRandomHistory(commits,dictionary):
    random.seed()
    history = []
    for commit in commits:
        temp = list(commit[2])
        for i in range(len(commit[2]),0,-1):
            name = "root/"+temp.pop(random.randrange(i))
            history.append(dictionary[name])
    return history

def constructHistory(commits,dictionary):
    random.seed()
    history = []
    for commit in commits:
        for file in commit[2]:
            name = "root/"+file
            history.append(dictionary[name])
    return history

def calculateFrequency(history,fsystem,flist):
    frequency = [0]*len(flist)
    for log in history:
        route = []
        idx = log
        while idx != -1:
            route.insert(0,idx)
            idx = fsystem[idx][0]
        for i in range(0,len(route)-1):
            sidx = route[i]
            didx = route[i+1]
            frequency[didx] += 1
    return frequency
            
    
def frequencyRanking(files,fsystem,frequency):
    freq = list(map(lambda s,f = frequency:(-f[s],s),files))
    freq.sort()
    return list(map(lambda s:s[1],freq))

def antLikeRanking(files,fsystem,pheromone):
    global evaRate
    freq = list(map(lambda s,f = pheromone:(-f[s],s),files))
    for file in files:
        pheromone[file] *= evaRate
    freq.sort()
    return list(map(lambda s:s[1],freq))

evaRate = 1
f = open(sys.argv[1],encoding='UTF8')
commits = []
i = 0

## construct log list
line = ""
name = ""
date = 0
print("construct commits")
while True:
    line = f.readline()
    if line == "\n": continue
    if not line: break
    date = int(line[5:-1])
    name = f.readline()[7:-1]
    files = []
    ##print("srcs")
    while True :
        line = f.readline()
        if line == "\n" : break
        files.append(line[0:-1])
    commits.append((date,name,files))
f.close()

print("construct file list")
fileList = constructFileList(commits)
print("construct file name list")
fileNameList = constructFileNameList(fileList)
print("construct file system")
fileSystem = constructFileSystem(fileList)

print("make a history")

dictionary = constructDictionary(fileList)
history = constructHistory(commits,dictionary)
f = open(sys.argv[1]+"_rs",'w',encoding='UTF8')
for i in range(0,101):
    evaRate = i/100
    print(i)
    ##print("calculate total sum of ranks using pheromone evaRate: ",evaRate)
    simpleTotRank = totRank(history,fileSystem,fileNameList,2,True)
    string = str(evaRate)+" "+str(simpleTotRank[1]/simpleTotRank[0])+" "+str((simpleTotRank[1]+simpleTotRank[2])/(simpleTotRank[0]+simpleTotRank[2]))+"\n"
    f.write(string)

f.close()
##print(averageRank(g,fileSystem))
    

