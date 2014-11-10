import pylab as plt
import pandas as pd
from numpy import array
from numpy import std

markers = ['o', 's', '*', 'x', '+', '>', '<', '_', 'h']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.75']

def get_mean(arrays):
    total = array([0]*len(arrays[0])) + arrays[0]
    for n in range(1, len(arrays)):
        total += arrays[n]
    means = total[:] / len(arrays)
    return means


def calc_sd(arrays, means):
    sds = []
    for n in range(len(arrays[0])):
        vector = []
        for arry in arrays:
            vector.append(arry[n])
        sds.append(std(vector))
    return array(sds)


def calc_se(arrays, sds):
    ses = sds / len(arrays)**0.5
    return ses


def lines_to_discard(filename):
    with open(filename) as datafile:
        lines = datafile.readlines()

    count = 0
    
    for line in lines:
        line = line.split(';')
        if line[0] == 'ScanArea.Name':
            return count
        else:
            count += 1


def get_dataframe(filename):
    dataframe = pd.read_csv(filename, sep = ";", skiprows = lines_to_discard(filename))
    return dataframe


def get_data_from_well(dataframe, well):
    return dataframe[dataframe['ScanArea.Name'] == well]


def make_triplicates(filename, wellslist, numbers, letters, errorbars = 'SE', measurement = 'BCA', show = False):
    df = get_dataframe(filename)
    for i in range(len(wellslist)):
        wells = wellslist[i]
        arrays = []
        for well in wells:
            well_data = get_data_from_well(df, well)
            arrays.append(well_data[measurement].values)
        means = get_mean(arrays)
        sds = calc_sd(arrays, means)
        ses = calc_se(arrays, sds)
        errors = {'SD': sds, 'SE': ses}
        plt.errorbar(well_data['TimestampInSeconds'].values / 3600, means,\
                     label = letters[wells[0][0]] + ', ' + numbers[wells[0][1:]],\
                     yerr = errors[errorbars], marker = markers[i], linewidth = 2, color = colors[i])
    plt.legend(loc = 4)
    plt.xlabel('Time (hours)')
    plt.ylabel(measurement)
    if show:
        plt.show()
    else:
        plt.savefig('static/showme.png')
    plt.clf()
   plt.clf()
