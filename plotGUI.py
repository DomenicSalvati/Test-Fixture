from pylab import *
import os
import scipy as sp
import numpy as np 
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

#----------------------------------------------------------------------------------------------------
# FFM Test fixture data analyser by Domenic Salvati
# Input dataAnalyser(path,'dataset') path being the file location of the data you wish to analyse, enter it as a string. ex. 'G:/'
# Dataset is a string that represents the data you want 'force' for force 'nozzle' for nozzle temp 'all' if you want everything
# All CSV files in that location will be plotted. Edit the various plot functions to change which columns are plotted and how the graphs 
# are presented. Timefix is there because the way the test fixture takes data is not constant. It takes a different amount of time
# every data point so this function makes the time plotted represent the actual amount of time that passed.
# Version 1.5
# Change log:
# Version 2.0: Now includes a GUI that makes plotting much easier
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
    if isinstance(dirList, str):
        plt.plot(dataTime,data[0])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
    else:
        plt.plot(dataTime,data[0], label=dirList[lister[i]])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)

    
def returnPlot(path,title,xLabel,yLabel,c):
    data,n = dataRipper(path) 
    for i in range(0,n):
         smoothedHTMTemp = 0
         smoothedHTMTemp = smooth(data[i],c)
         Plotter(smoothedHTMTemp,title,xLabel,yLabel, i)
    if not isinstance(dirList, str):
        plt.legend()
    plt.show()

    
def browseButton(buttonType):
    global folderPath
    if buttonType: 
        filename = filedialog.askdirectory()
        folderPath = filename + '/'
    else:
        filename = filedialog.askopenfilename()
        folderPath = filename       

def buttonHide(*args):
    if dataColumn.get():
        plotButton.state(['!disabled'])
    else:
        plotButton.state(['disabled'])

root = Tk()
root.title("Dom Plot")
mainFrame = ttk.Frame(root, padding="3 3 12 12")
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

title = StringVar()
xLabel = StringVar()
yLabel = StringVar()
global dataColumn
dataColumn = StringVar()
fileStyle = BooleanVar()

titleEntry = ttk.Entry(mainFrame, width=10, textvariable=title)
xLabelEntry = ttk.Entry(mainFrame, width=7, textvariable=xLabel)
yLabelEntry = ttk.Entry(mainFrame, width=7, textvariable=yLabel)
dataColumnEntry = ttk.Entry(mainFrame, width=3, textvariable=dataColumn)


titleEntry.grid(column=1, row=1)
xLabelEntry.grid(column=1, row=2)
yLabelEntry.grid(column=1, row=3)
dataColumnEntry.grid(column=1, row=4)

ttk.Checkbutton(mainFrame, text="Multiple files?", variable=fileStyle).grid(column=3, row=1)

ttk.Button(mainFrame, text="Select file or folder", command= lambda: browseButton(fileStyle.get())).grid(column=3, row=2, sticky=W)

ttk.Label(mainFrame, text="Title").grid(column=2, row=1, sticky=W)
ttk.Label(mainFrame, text="X Label").grid(column=2, row=2, sticky=W)
ttk.Label(mainFrame, text="Y Label").grid(column=2, row=3, sticky=W)
ttk.Label(mainFrame, text="Data Column").grid(column=2, row=4, sticky=W)

global plotButton
plotButton = ttk.Button(mainFrame, text="Plot", command=lambda: returnPlot(folderPath,title.get(),xLabel.get(),yLabel.get(),int(dataColumn.get())))
plotButton.grid(column=3, row=3, sticky=W)
plotButton.state(['disabled'])

dataColumn.trace('w', buttonHide)

root.mainloop()
    

    
    
    