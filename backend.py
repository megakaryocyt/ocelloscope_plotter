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


def make_simple_plot(filename, wells, numbers, letters, measurement = 'BCA'):
    df = get_dataframe(filename)
    for n in range(len(wells)):
        well_data = get_data_from_well(df, wells[n])
        plt.plot(well_data['TimestampInSeconds'].values / 3600, well_data[measurement],\
                 marker = markers[n], label = letters[wells[n][0]] + ', ' + numbers[wells[n][1:]] + ', ' + wells[n])
    plt.ylabel(measurement)
    plt.xlabel('Time (Hours)')
    plt.legend(loc = 4)
    plt.show()
    plt.clf()

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

def make_combined_triplicates(filenames, wellslist, numbers, letters, measurement = 'BCA', show = False):
    dataframes = [get_dataframe(x) for x in filenames]
    for i in range(len(wellslist)):
        wells = wellsList[i]
        arrays = []
        for n in range(len(dataframes)):
            for well in wells[n]:
                well_data = get_data_from_well(dataFrames[n], well)
                if len(well_data.values) > 49:
                    want = [x for x in range(len(well_data)) if (x < 24 and x % 2 == 0) or x >= 24]
                    arrays.append(array([well_data[measurement].values[y] for y in want]))
                else:
                    arrays.append(well_data[measurement].values[:-1])
        means = get_mean(arrays)
        sds = calc_sd(arrays, means)
        ses = calc_se(arrays, sds)
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
