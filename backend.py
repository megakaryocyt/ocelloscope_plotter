# Make sure that plots can be produced without an X server running
import matplotlib
matplotlib.use('Agg')
# Import what is needed to plot things
import pylab as plt
from numpy import array
from numpy import std

markers = ['o', 's', '*', 'x', '+', '>', '<', '_', 'h']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.75']

class well:
    def __init__(self, name):
        self.name = name
        self.pts = []

    def get_name(self):
        """
        Returns the name of the well as a string.
        """
        return str(name)

    def get_measurements(self, axis):
        """
        Returns a list of either the x values (time)
        or the y values (BCA). Takes the argument
        axis, which needs to be set to 'x' or 'y', 
        depending on the values needed.
        """
        if axis == 'x':
            return array([p[0] for p in self.pts])
        elif axis == 'y': 
            return array([p[1] for p in self.pts])
        else:
            print "Call this function with either 'x' or 'y' as argument"
            return 0

    def add_point(self, secs, bca):
        """
        Method to add measurements to the well class.
        Takes seconds as the first argument which is converted
        to hours and added to the corresponding array. BCA is given
        as the second argument, SESA and TA are not supported.
        """
        hrs = float(secs) / 3600
        self.pts.append((hrs, float(bca)))


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
    """
    Parses a .csv file created by the ocelloscope,
    and detects where the actual measurements begin.
    Returns the number of lines that need to be 
    discarded as an integer.
    """
    with open(filename) as datafile:
        lines = datafile.readlines()

    count = 0
    
    for line in lines:
        line = line.split(';')
        if line[0] == 'ScanArea.Name':
            return count
        else:
            count += 1


def parse_csv(filename):
    """
    Parses a .csv file from the Ocelloscope and returns
    a dict for each well.
    """
    titer_plate = {}

    to_discard = lines_to_discard(filename)

    with open(filename) as csv_file:
        lines = csv_file.readlines()[to_discard:]

    for line in lines:
        cols = line.split(';')
        if titer_plate.has_key(cols[0]):
            titer_plate[cols[0]].add_point(cols[-1], cols[8])
        else:
            titer_plate[cols[0]] = well(cols[0])

    return titer_plate


def make_triplicates(\
    filename,\
    wells_list,\
    numbers,\
    letters,\
    errorbars = 'sd',\
    measurement = 'BCA'):
    """
    Plots out a combined graph with errorbars for every list of wells
    given in the master list (wells_list). Afterwards saves it in the
    static folder. Returns nothing.
    """
    plate = parse_csv(filename)

    for wells in wells_list:
        measurements = [plate[x].get_measurements('y') for x in wells]
        means = get_mean(measurements)    
        sds = calc_sd(measurements, means)
        ses = calc_se(measurements, sds)

        if errorbars == 'sd':
            err = sds
        else:
            err = ses

        lbl = letters[wells[0][0]] + ', ' + numbers[wells[0][1:]]

        t = plate[wells[0]].get_measurements('x')
        plt.errorbar(t, means, yerr = err, label = lbl)

    plt.savefig('static/showme.png')
