from pylab import *
import os
import scipy as sp
import numpy as np 
import matplotlib.pyplot as plt 


#----------------------------------------------------------------------------------------------
# This code allows you to plot multiple things in the same plot. It's a nice way to present data.
# In order to use this, put all the files you want to plot in the same folder. 
# Put them in alphabetical order that you want them to be plotted in because that is how the program sorts them
# You can just number them, that's easiest
# If you look in the multiplot function you can see the general structure of what it does. Just add or take away plots
# if you want more or less.
# Otherwise it works pretty much the same as the data analyser.
#----------------------------------------------------------------------------------------------

def dataRipper(path):
    lister = []
    directory = os.path.join(path)
    dirList = os.listdir(directory)
    dirList = sorted(dirList)
    for i in range(0,len(dirList)):
        if dirList[i].endswith(".csv"):
            lister.append(i)        
    data = 0
    data = [np.genfromtxt(directory + dirList[lister[j]],delimiter=',') for j in range(len(lister))]
    return data,len(lister)
def smooth(dataUse,column):
    for i in range(0,len(dataUse[:,column])):
        if i < 3:
            if abs(dataUse[i,column] -((dataUse[i+3,column] + dataUse[i+2,column] + dataUse[i+1,column]/3))) > 3: 
                dataUse[i,column] = (dataUse[i+5,column] + dataUse[i+4,column])/2
        elif i > len(dataUse[:,column]) - 6:
            if abs(dataUse[i,column] -((dataUse[i-3,column] + dataUse[i-2,column] + dataUse[i-1,column]/3))) > 3:  
                dataUse[i,column] = (dataUse[i-5,column] + dataUse[i-4,column])/2  
        else:
            if abs(dataUse[i,column] -((dataUse[i+3,column] + dataUse[i+2,column] + dataUse[i+1,column] + dataUse[i-1,column] + dataUse[i-2,column] + dataUse[i-3,column])/6)) > 3:
                dataUse[i,column] = (dataUse[i+5,column] + dataUse[i-5,column])/2
    return dataUse[:,column],dataUse[:,0]


def timeFix(data):
    calcData = data[1] * 0.001
    dataTime = sp.zeros(len(calcData))
    dataTime[0] = calcData[0] 
    for f in range(1,len(calcData)):
        dataTime[f] = calcData[f] + dataTime[f-1]
    return dataTime
    
def multiPlot(path):
    fig = plt.figure()
    host = fig.add_subplot(111)
    data,n = dataRipper(path)
    par1 = host.twinx()
    
    host.set_xlabel("Time(s)")
    host.set_ylabel("Force(lbs)")
    par1.set_ylabel("Nozzle Temperature(C)")
    host.set_ylim(0,15)
    par1.set_ylim(240,255)
    host.set_title('Force and Temperature at 8mm/s')
    
    color1 = plt.cm.viridis(0)
    color2 = plt.cm.viridis(0.5)
    color3 = plt.cm.viridis(0.9)
    color4 = plt.cm.viridis(0.2)
    
    force1 = smooth(data[0],1)
    temp1 = smooth(data[0],7)
    #botTemp1 = smooth(data[0],4)
    force2 = smooth(data[1],1)
    temp2 = smooth(data[1],3)
    force3 = smooth(data[2],1)
    temp3 = smooth(data[2],5)
    time1 = timeFix(force1)
    time2 = timeFix(force2)
    time3 = timeFix(force3)

    p1, = par1.plot(time1 ,temp1[0], color=color1,label="Fortus Temp")
    #p7, = par1.plot(time1 ,botTemp1[0], color=color4,label="Dual Nichrome Bottom Temp")
    p2, = host.plot(time1,force1[0],'--', color=color1, label="Fortus Force")
    p3, = par1.plot(time2,temp2[0], color=color2, label="Hybrid Temp")
    p4, = host.plot(time,force2[0],'--', color=color2, label="Hybrid Force")
    p5, = par1.plot(time3,temp3[0], color=color3, label="25 mm HTM Temp")
    p6, = host.plot(time3,force3[0],'--', color=color3, label="25 mm HTM Force")
    
    lns = [p1,p2,p3,p4,p5,p6]
    host.legend(handles=lns, loc=(1.15,0))

def multiPlot2(path):
    fig = plt.figure()
    host = fig.add_subplot(111)
    data,n = dataRipper(path)
    par1 = host.twinx()
    
    host.set_xlabel("Time(s)")
    host.set_ylabel("Force(lbs)")
    par1.set_ylabel("Nozzle Temperature(C)")
    host.set_title('Hybrid Nozzle Trial Before Failure(17mm/s)')
    host.set_ylim(0,40)
    par1.set_ylim(240,260)
    
    color1 = plt.cm.viridis(0)
    color2 = plt.cm.viridis(0.5)
    color3 = plt.cm.viridis(0.9)
    
    force1 = smooth(data[0],1)
    temp1 = smooth(data[0],7)
    time = timeFix(force1)
    
    p1, = par1.plot(2*time,temp1[0], color=color1,label="Hybrid Temp")
    p2, = host.plot(2*time,force1[0],'--', color=color1, label="Hybrid Force")

    
    lns = [p1, p2]
    host.legend(handles=lns, loc='best')
