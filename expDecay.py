from pylab import *
import os
import scipy as sp
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

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
        data = 0
        data = [np.genfromtxt(directory,delimiter=',')]
        lister = [0]
    return data,len(lister)


def smooth(dataUse,column):
    for i in range(0,len(dataUse[:,column])):
        if i < 3:
            if abs(dataUse[i,column] -((dataUse[i+3,column] + dataUse[i+2,column] + dataUse[i+1,column]/3))) > 6: 
                dataUse[i,column] = (dataUse[i+5,column] + dataUse[i+4,column])/2
                if dataUse[i,column] > 600:
                    dataUse[i,column] = dataUse[i-1,column]
        elif i > len(dataUse[:,column]) - 6:
            if abs(dataUse[i,column] -((dataUse[i-3,column] + dataUse[i-2,column] + dataUse[i-1,column]/3))) > 6:  
                dataUse[i,column] = (dataUse[i-5,column] + dataUse[i-4,column])/2  
                if dataUse[i,column] > 600:
                    dataUse[i,column] = dataUse[i-1,column]
        else:
            if abs(dataUse[i,column] -((dataUse[i+3,column] + dataUse[i+2,column] + dataUse[i+1,column] + dataUse[i-1,column] + dataUse[i-2,column] + dataUse[i-3,column])/6)) > 6:
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
    
def func(x, a, b, c, d,f):
    return a*np.exp(-b*x)+ d*np.exp(-f * x) + c
    
def lineFit(data,n):
    dataSmooth = smooth(data[0],1)
    t = timeFix(dataSmooth)
    coef,notCoef = curve_fit(func,t,dataSmooth[0])
    y = coef[0] * e**(-coef[1] * t) + coef[3] * e**(-coef[4] * t) + coef[2]
    plt.plot(t,dataSmooth[0])
    plt.plot(t,y)
    plt.show()
    r = np.sqrt(np.diag(notCoef))
    print(str(coef[0]) + '              e^             ' + str(-coef[1]) + '       x         +     ' + str(coef[3]) + '              e^             ' + str(-coef[4]) + '       x         +     ' + str(coef[2]))
    print('r = ' + str(r))
    with open('C:/Users/Domenic/desktop/work/pressure decay/DDS 3.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(coef)

def expDecay(path):
    data,n = dataRipper(path)
    lineFit(data,n)