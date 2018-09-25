from pylab import *
import matplotlib.pyplot as plt
from scipy import stats
import scipy as sp
import os
import numpy as np


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

def modeFinder(path):
    data,n = dataRipper(path)
    modes = []
    for i in range(n):
        setMode = float(sp.stats.mode(data[i][:,1])[0])
        modes.append(setMode)
    return modes

def interpolator(path):
    modes = modeFinder(path)
    for i in range(1,len(modes)-1):
        if modes[i] < modes[i-1]:
            modes[i] = (modes[i+1] + modes[i-1])/2
    return modes
 

HTM30 = sp.array([[2,4,6,8,10,12,14,16,18,19,20,21],interpolator('G:/30 mm/')])
plt.plot(HTM30[0],HTM30[1],label='30mm HTM')

HTM35 = sp.array([[2,4,6,8,10,12,14,16,18,20,21,22,23],interpolator('G:/35 mm/')])
plt.plot(HTM35[0],HTM35[1],label='35mm HTM')

HTM3080g = sp.array([[2,4,6,8,10,12,14,16,18,20],interpolator('G:/30mm80g/')])
plt.plot(HTM3080g[0],HTM3080g[1],label='30mm 80g HTM')

HTM25 = sp.array([[2,4,6,8,10,12,14,16],interpolator('G:/25mm8-2-2018/')])
plt.plot(HTM25[0],HTM25[1],label='25mm HTM')

hybrid = sp.array([[2,4,6,8,10,12,14,16,18],interpolator('G:/hybrid8-1-2018/')])
plt.plot(hybrid[0],hybrid[1],label='Hybrid')

nichrome = sp.array([[2,4,6,8,10,12,14],interpolator('G:/nichrome7-31-2018/')])
plt.plot(nichrome[0],nichrome[1],label='Nichrome')

fortus = sp.array([[2,4,6,8,10,12],interpolator('G:/fortus7-24-2018/')])
plt.plot(fortus[0],fortus[1],label='Fortus')

HTM15 = sp.array([[2,4,6,8,10,12],interpolator('G:/15mm8-2-2018/')])
plt.plot(HTM15[0],HTM15[1],label='15mm HTM')

plt.title('Force vs. Speed')
plt.xlabel('Speed(mm/s)')
plt.ylabel('Force(lbs)')
plt.legend()









































