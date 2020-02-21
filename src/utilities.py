# coding = utf-8
# __author__ = ''

import math
import random
import matplotlib.pyplot as plt
import time
import xlwt


'''
Functions:
1. Define Class Vehicle and Cell
2. read cell data
3. Plot graph of cells

'''
dec = 3

'''
    class Vehicle has method load & cancel & get_route
    it also has attributes including maxCapacity & cells
'''


class Vehicle:
    def __init__(self, max_capacity):
        self.maxCapacity = max_capacity
        self.cells = []
        self.workload = 0

    def load(self, cell):
        self.cells.append(cell)
        self.workload += cell.ord

    def cancel(self, cell):
        self.cells.remove(cell)
        self.workload -= cell.ord

    def get_route(self):
        cell_list = [i.id for i in self.cells]
        order = str(cell_list[i] for i in range(len(cell_list)))
        return str(len(self.cells)+' cells:'+order)

'''Every cell has an array of neighbors
    All those cells are sorted according to their distances from one specific point
    first 4~6 cells are assumed as neighbors'''


class Cell:
    def __init__(self, identification, lng, lat, order_num):
        self.x = lng
        self.y = lat
        self.ord = order_num
        self.id = identification
        self.ang = 0.0
        self.nb = []

    def set_ang(self, angle):
        self.ang = angle


# Manhaton Distance

def m_dist(dot1, dot2):
    temp = abs(dot1.x-dot2.x)+abs(dot1.y-dot2.y)
    return temp


def read_cells(num, no):
    if num < 50:
        temp = 'small'
    else:
        temp = 'large'
    f = open('tester_cell_'+temp+'_scale/CellSource_'+str(num)+'_'+str(no)+'.txt', 'r')
    cells = []
    f.readline()
    for line in f:
        l = line.decode()
        content = l.split(' ')
        cells.append(Cell(content[0], round(float(content[1]), dec), round(float(content[2]), dec), int(content[3])))

    f.close()
    return cells


''' ---READ TEST---
all_cell = read_cells(10, 1)
for cell in all_cell:
    print cell.id, cell.x, cell.y, cell.ord
'''

# count the load of a bunch of cells


def load_count(route):
    route_c = route[:]
    total_load = 0
    for i in route_c:
        total_load += i.ord

    return total_load


# sort polar angle

def polar_angle(depot, cell):
    cell_list = cell[:]

    for dot in cell_list:
        dot.set_ang(math.atan2(dot.y-depot.y, dot.x-depot.x))
    sorted_list = sorted(cell_list, key=lambda cell: cell.ang)

    return sorted_list


# Generate Initial Solution
# Every time you call initial_sol_sweep you will get another fleet assignment


def initial_sol_sweep(cells, numVehicle, maxCapacity):
    sweep_list = polar_angle(cells[0], cells[1:])

    tot_load = load_count(sweep_list)
    criteria = int(tot_load/numVehicle)

    ''' ---TEST SWEEP_LIST---
    print criteria
    for i in sweep_list:
        print i.id
    '''

    length = len(sweep_list)
    axi = random.randrange(0, length)
    v = 0
    fleet = []
    for i in range(numVehicle):
        fleet.append(Vehicle(maxCapacity))
    i = 0
    while i < length and v < numVehicle:
        while fleet[v].workload <= criteria and i < length:
            if axi >= length:
                axi = 0
            fleet[v].load(sweep_list[axi])
            axi += 1
            i += 1
        v += 1

    for i, v in enumerate(fleet):
        print 'Vehicle {0} in charges:'.format(i)
        for j in v.cells:
            print j.id
        print v.workload, ';'

    return fleet, tot_load

''' ---TEST SWEEP---
    for i, v in enumerate(fleet):
        print 'Vehicle {0} in charges:'.format(i)
        for j in v.cells:
            print j.id
        print v.workload, ';'
'''

''' --- TEST INITIAL_SOL_SWEEP---
all_cell = read_cells(35, 5)
initial_sol_sweep(all_cell, 4, 1000)
'''


''' Plotting randomly generated cells in xy-coordinates
    Depot has be set as the midpoint of the whole graph'''


def plot_points(cells, xmin, xmax, ymin, ymax):

    x = []
    y = []
    dots = cells[:]
    for dot in dots:
        x.append(dot.x)
        y.append(dot.y)
    plt.plot(x[0], y[0], 'bo')
    plt.plot(x[1:], y[1:], 'ro')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.show()


''' ---PLOT TEST---
plot_points(all_cell, 0, 100, 0, 100)
'''

'''In this part, we find neighbors of each cell
    the relationship of neighbor are given by a matrix consists of 0 and 1
    where 1 stands for they are neighbors'''

# Write sheet of neighbor relationships
def neighbor_generator():
    for num in range(10, 40, 5):
        for ind in range(20):
            all_cell = read_cells(num, ind+1)
            n = len(all_cell)

            class Set:
                def __init__(self, dot1, dot2):
                    self.id = dot2.id
                    self.dd = m_dist(dot1, dot2)

            filename = xlwt.Workbook()
            sheet = filename.add_sheet("neighbor")
            for i in range(n):
                sheet.write(0, i+1, all_cell[i].id)
                sheet.write(i+1, 0, all_cell[i].id)

            for i in all_cell:
                nid = []
                for j in all_cell:
                    if i != j:
                        nid.append(Set(i, j))
                    else:
                        sheet.write(int(i.id), int(j.id), 0)

                nid = sorted(nid, key=lambda Set: Set.dd)
                for j in range(4):
                    i.nb.append(nid[j])
                for j in all_cell:
                    if j in i.nb:
                        sheet.write(int(i.id), int(j.id), 1)
                    else:
                        sheet.write(int(i.id), int(j.id), 0)
            filename.save("neighbor_"+str(num)+"_"+str(ind+1)+".xls")


'''---------------  Generate Dist Excel -----------------
                sheet.write(int(i.id), int(j.id), m_dist(i, j))
        filename.save("dist_"+str(num)+"_"+str(ind+1)+".xls")
'''

# plot_points(all_cell, 0, 100, 0, 100)
