from pylab import *
import os
import scipy as sp
import numpy as np 
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------
# FFM Test fixture data analyser by Domenic Salvati
# Input dataAnalyser(path,'dataset') path being the file location of the data you wish to analyse, enter it as a string. ex. 'G:/'
# Dataset is a string that represents the data you want 'force' for force 'nozzle' for nozzle temp 'all' if you want everything
# All CSV files in that location will be plotted. Edit the various plot functions to change which columns are plotted and how the graphs 
# are presented. Timefix is there because the way the test fixture takes data is not constant. It takes a different amount of time
# every data point so this function makes the time plotted represent the actual amount of time that passed.
# Version 1.5
# Change log:
# Version 1.5: Time is now correctly accounted for
# Version 1.4: Files are sorted in alphabetical order now
# Version 1.3: improved smoothing algorithm further 7/10/2018
# Version 1.2: smoothing algorithm is now more refined
#              added automated legends 7/6/2018
# Version 1.1: included middle link temp and feed block temp 7/5/2018
#----------------------------------------------------------------------------------------------------

def dataRipper(path):
    global dirList
    global lister
    lister = []
    directory = os.path.join(path)
    try:
        dirList = os.listdir(directory)
        dirList = sorted(dirList)
        for i in range(0,len(dirList)):
            if dirList[i].endswith(".csv"):
                lister.append(i)
        data = 0
        data = [np.genfromtxt(directory + dirList[lister[j]],delimiter=',') for j in range(len(lister))]
    except:
        dirList = directory
        data = 0
        data = [np.genfromtxt(directory,delimiter=',')]
        lister = [0]

    return data,len(lister)

def smooth(dataUse,column):
    for i in range(0,len(dataUse[:,column])):
        if i < 3:
            if abs(dataUse[i,column] -((dataUse[i+3,column] + dataUse[i+2,column] + dataUse[i+1,column]/3))) > 3: 
                dataUse[i,column] = (dataUse[i+5,column] + dataUse[i+4,column])/2
                if dataUse[i,column] > 600:
                    dataUse[i,column] = dataUse[i-1,column]
        elif i > len(dataUse[:,column]) - 6:
            if abs(dataUse[i,column] -((dataUse[i-3,column] + dataUse[i-2,column] + dataUse[i-1,column]/3))) > 3:  
                dataUse[i,column] = (dataUse[i-5,column] + dataUse[i-4,column])/2  
                if dataUse[i,column] > 600:
                    dataUse[i,column] = dataUse[i-1,column]
        else:
            if abs(dataUse[i,column] -((dataUse[i+3,column] + dataUse[i+2,column] + dataUse[i+1,column] + dataUse[i-1,column] + dataUse[i-2,column] + dataUse[i-3,column])/6)) > 3:
                dataUse[i,column] = (dataUse[i+5,column] + dataUse[i-5,column])/2
                if dataUse[i,column] > 600:
                    dataUse[i,column] = dataUse[i-1,column]
    return dataUse[:,column],dataUse[:,0]

def timeFix(data):
    calcData = data[1] * 0.001
    dataTime = sp.zeros(len(calcData))
    dataTime[0] = calcData[0] 
    for f in range(1,len(calcData)):
        dataTime[f] = calcData[f] + dataTime[f-1]
    return dataTime
    

def Plotter(data,title,x,y,i):    
    dataTime = timeFix(data)
    plt.plot(dataTime,data[0], label=dirList[lister[i]])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)

def forcePlot(data,n):
    for i in range(0,n):
        smoothedForce = 0
        smoothedForce = smooth(data[i],1)
        Plotter(smoothedForce,'Force Over Time','Time(s)','Force(lbs)',i)
    plt.legend()
    plt.show()
    
def nozzleTempPlot(data,n):
    for i in range(0,n):
        smoothedNozzleTemp = 0
        smoothedNozzleTemp = smooth(data[i],6)
        Plotter(smoothedNozzleTemp,'Bottom Nozzle Temp Over Time','Time(s)','Temp(C)', i)
    plt.legend()
    plt.show()

def middleLinkPlot(data,n):
    for i in range(0,n):
        smoothedMiddleLink = 0
        smoothedMiddleLink = smooth(data[i],5)
        Plotter(smoothedMiddleLink,'Middle Nozzle Temp Over Time','Time(s)','Temp(C)',i)
    plt.legend()
    plt.show()
    
def feedBlockPlot(data,n):
    for i in range(0,n):
        smoothedFeedBlock = 0
        smoothedFeedBlock = smooth(data[i],4)
        Plotter(smoothedFeedBlock,'Top Nozzle Temp Over Time','Time(s)','Temp(C)',i)
    plt.legend()
    plt.show()
    
def HTMPlot(data,n):
    for i in range(0,n):
        smoothedHTMTemp = 0
        smoothedHTMTemp = smooth(data[i],8)
        Plotter(smoothedHTMTemp,'HTM Temp Over Time','Time(s)','Temp(C)', i)
    plt.legend()
    plt.show()

    
def allPlot(data,n):
    forcePlot(data,n)
    nozzleTempPlot(data,n)
    middleLinkPlot(data,n)
    feedBlockPlot(data,n)
    HTMPlot(data,n)
    
def use(flag,data,n):
    switcher = {
        'force': forcePlot,
        'nozzle': nozzleTempPlot,
        'middle': middleLinkPlot,
        'feed': feedBlockPlot,
        'HTM': HTMPlot,
        'all': allPlot,
    }
    switcher.get(flag)(data,n)
   
def dataAnalyser(path,flag):
    data,n = dataRipper(path)
    use(flag,data,n)
    