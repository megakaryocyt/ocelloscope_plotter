import pylab as plt
import pandas as pd
from numpy import array
from numpy import std

markers = ['o', 's', '*', 'x', '+', '>', '<', '_', 'h']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

def getMean(arrays):
    total = array([0]*len(arrays[0])) + arrays[0]
    for n in range(1, len(arrays)):
        total += arrays[n]
    means = total[:] / len(arrays)
    return means


def calcSD(arrays, means):
    sds = []
    for n in range(len(arrays[0])):
        vector = []
        for arry in arrays:
            vector.append(arry[n])
        sds.append(std(vector))
    return array(sds)


def calcSE(arrays, sds):
    ses = sds / len(arrays)**0.5
    return ses


def linesToDiscard(filename):
    with open(filename) as dataFile:
        lines = dataFile.readlines()
    
    count = 0
    
    for line in lines:
        line = line.split(';')
        if line[0] == 'ScanArea.Name':
            return count
        else:
            count += 1


def getDataFrame(filename):
    dataFrame = pd.read_csv(filename, sep = ";", skiprows = linesToDiscard(filename))
    return dataFrame


def getDataFromWell(dataFrame, well):
    return dataFrame[dataFrame['ScanArea.Name'] == well]


def makeSimplePlot(filename, wells, numbers, letters, measurement = 'BCA'):
    df = getDataFrame(filename)
    for n in range(len(wells)):
        wellData = getDataFromWell(df, wells[n])
        plt.plot(wellData['TimestampInSeconds'].values / 3600, wellData[measurement],\
                 marker = markers[n], label = letters[wells[n][0]] + ', ' + numbers[wells[n][1:]] + ', ' + wells[n])
    plt.ylabel(measurement)
    plt.xlabel('Time (Hours)')
    plt.legend(loc = 4)
    plt.show()
    plt.clf()

def makeTriplicates(filename, wellsList, numbers, letters, measurement = 'BCA', show = False):
    df = getDataFrame(filename)
    for i in range(len(wellsList)):
        wells = wellsList[i]
        arrays = []
        for well in wells:
            wellData = getDataFromWell(df, well)
            arrays.append(wellData[measurement].values)
        means = getMean(arrays)
        sds = calcSD(arrays, means)
        ses = calcSE(arrays, sds)
        plt.errorbar(array(range(len(means)))/2.0, means,\
                     label = letters[wells[0][0]] + ', ' + numbers[wells[0][1:]],\
                     yerr = ses, marker = markers[i], linewidth = 2, color = colors[i])
    plt.legend(loc = 4)
    plt.xlabel('Time (hours)')
    plt.ylabel(measurement)
    if show:
        plt.show()
    else:
        plt.savefig('static/showme.png')
    plt.clf()

def makeCombinedTriplicates(filenames, wellsList, numbers, letters, measurement = 'BCA', show = False):
    dataFrames = [getDataFrame(x) for x in filenames]
    for i in range(len(wellsList)):
        wells = wellsList[i]
        arrays = []
        for n in range(len(dataFrames)):
            for well in wells[n]:
                wellData = getDataFromWell(dataFrames[n], well)
                if len(wellData.values) > 49:
                    want = [x for x in range(len(wellData)) if (x < 24 and x % 2 == 0) or x >= 24]
                    arrays.append(array([wellData[measurement].values[y] for y in want]))
                else:
                    arrays.append(wellData[measurement].values[:-1])
        means = getMean(arrays)
        sds = calcSD(arrays, means)
        ses = calcSE(arrays, sds)
        plt.errorbar(array(range(len(means))) / 2.0, means,\
                     label = letters[wells[1][0][0]] + ', ' + numbers[wells[1][0][1:]],\
                     yerr = sds, marker = markers[i], linewidth = 2)
        plt.legend(loc = 4)
    plt.xlabel('Time (hours)')
    plt.ylabel(measurement)
    if show:
        plt.show()
    else:
        plt.savefig('static/showme.png')
    plt.clf()