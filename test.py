#-*- coding: utf-8 -*-

from datetime import datetime
import random
import math


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

def constructFileSystem(flist):
    fsystem = [[-1]]
    for i in range(1,len(flist)):
        parentfile = flist[i][:flist[i].rindex("/")]
        parPosit = flist.index(parentfile)
        fsystem[parPosit].append(i)
        fsystem.append([parPosit])
    return fsystem

def totRank(history,fsystem,rankFunc = None):
    frequency = None
    if (rankFunc == 1) | (rankFunc == 2):
        frequency = [0]*len(fsystem)
    totRank = 0
    totTry = 0
    for log in history:
        route = []
        idx = log
        while idx != -1:
            route.insert(0,idx)
            idx = fsystem[idx][0]
        for i in range(0,len(route)-1):
            sidx = route[i]
            didx = route[i+1]
            Files = fsystem[sidx][1:]
            if len(Files) <= 1:
                continue
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
            totRank += sortedFiles.index(didx)+1
    if (rankFunc == 1) | (rankFunc == 2):
        frequency.sort(reverse=True)
        print(frequency[0])
    return (totTry,totRank)
                
def constructRandomHistory(commits,flist):
    random.seed()
    history = []
    for commit in commits:
        temp = list(commit[2])
        for i in range(len(commit[2]),0,-1):
            name = "root/"+temp.pop(random.randrange(i))
            history.append(flist.index(name))
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
f = open("C:\SBSE\AntLog")
commits = []
i = 0

## construct log list
line = ""
name = ""
date = datetime.today()
print("construct commits")
while True:
    line = f.readline()
    if line == "COMMIT\n" :
        ##print("Find commit")
        name = f.readline()[:-1]
        date = datetime.strptime(f.readline()[:-1],"%a, %d %b %Y %H:%M:%S %z")
    else :
        files = []
        ##print("srcs")
        while True :
            if not line : break
            if line == "\n" : break
            files.append(line[0:-1])
            line = f.readline()
        if len(files) > 0:
            commits.append((date,name,files))
    if not line: break
f.close()

print("construct file list")
fileList = constructFileList(commits)

print("construct file system")
fileSystem = constructFileSystem(fileList)
totFiles = 0
totFolder = 0
for files in fileSystem:
    if len(files) > 2 :
        totFolder += 1
        totFiles+=len(files)-1
print("avgFiles",totFiles/totFolder)
frequency = [0 for _ in range(len(fileList))]

print("make a random history")
randHistory = constructRandomHistory(commits,fileList)
cal = calculateFrequency(randHistory,fileSystem,fileList)

print("calculate total sum of ranks using default")
simpleTotRank = totRank(randHistory,fileSystem)
print("totTry: ",simpleTotRank[0],
      "totRank",simpleTotRank[1]," avg: ",simpleTotRank[1]/simpleTotRank[0])

print("calculate total sum of ranks using frequency")
simpleTotRank = totRank(randHistory,fileSystem,1)
print("totTry: ",simpleTotRank[0],
      "totRank",simpleTotRank[1]," avg: ",simpleTotRank[1]/simpleTotRank[0])

for i in range(10):
    evaRate -= 0.001
    print("calculate total sum of ranks using pheromone evaRate: ",evaRate)
    simpleTotRank = totRank(randHistory,fileSystem,2)
    print("totTry: ",simpleTotRank[0],
      "totRank",simpleTotRank[1]," avg: ",simpleTotRank[1]/simpleTotRank[0])
    


##print(averageRank(g,fileSystem))
    
