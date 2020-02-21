# __author__ = ''

import random
import math
import time
from utilities import *
from collections import deque
from gurobipy import *

TimeLimit = 3


class Candidate:
    def __init__(self, fleet):
        self.fleet = fleet
        self.max_time = max(i.service_time for i in self.fleet)
        self.min_time = min(i.service_time for i in self.fleet)
        self.tot = sum(i.service_time for i in self.fleet)
        self.balance = get_var(fleet, self.tot)


# get the vehicle with the maximum workload
def max_load(fleet):
    return max(i.workload for i in fleet)

# get the vehicle with the minimum workload
def min_load(fleet):
    return min(i.workload for i in fleet)

# calculate variation between workloads of vehicles in a solution
def get_var(fleet, tot_load):
    average = tot_load/len(fleet)
    sq = 0
    for i in fleet:
        sq += (i.workload-average)**2
    return math.sqrt(sq)


def generate_candidate(best, tabu_list, points):
    tot_load = best.tot
    case0 = best[:]
    fleet0 = case0.fleet
    var0 = get_var(fleet0, tot_load)
    v0_num = len(fleet0)
    r = []
    l = []
    cr0 = True
    start = time.clock()
    random.seed()
    while cr0:
        r[0] = random.randrange(v0_num)
        r[1] = (r[0]+random.randrange(v0_num)) % v0_num
        cr1 = True
        while cr1:
            for i in (0, 1):
                if len(fleet0[r[i]].cells) > 0:
                    l[i] = min(j.ord for j in fleet0[r[i].cells])
                else:
                    l[i] = False
            if l[0]:
                fleet0[r[0]].cancel(l[0])
                fleet0[r[1]].load(l[0])
            if l[1]:
                fleet0[r[1]].cancel(l[1])
                fleet0[r[0]].load(r[1])
            if get_var(fleet0, tot_load) < var0:
                case0.fleet = fleet0
                return case0.fleet
            elif not l[1] and not l[0]:
                cr1 = False

        if time.clock()-start > TimeLimit:
            cr0 = False

    return

    # return the solution with the min Object Value in candidates


def local_best_candidate(candidates):
    best_candidate = candidates[0]
    for cd in candidates[1:]:
        if cd.tot < best_candidate.tot:
            best_candidate = cd

    return best_candidate


def result_output(solution, no):
    seq = []
    for i, v in enumerate(solution.fleet):
        s = ''
        s += 'Vehicle '+str(i)+' takes charge of:'
        for j in v.cells:
            s += j.id
        s += '\n'
        seq.append(s)
    with open('solution'+no+'.txt', 'rw+') as f:
        f.writelines(seq)


''' the main search function '''
def search(points, maxIteration, maxTabu, numVehicle, maxCandidate, maxCapacity):

    best = Candidate(initial_sol_sweep(points, numVehicle, maxCapacity))
#    taboo_list = deque([])

#    candidates = []
    while maxIteration > 0:
        temp = Candidate(initial_sol_sweep(points, numVehicle, maxCapacity))
        # results_output(10, maxIteration, temp.fleet)
        if temp.tot < best.tot:
            best = temp
        maxIteration -= 1

#        for index in range(0, maxCandidate):
#            candidates.append(generate_candidate(best, taboo_list, points))
#        best_candidate = local_best_candidate(candidates)
#        if best_candidate.workload < best.workload:
#            best = best_candidate
#            if len(taboo_list) < maxTabu:
#                taboo_list.append(best)
#            else:
#                taboo_list.popleft()
#        maxIteration -= 1

    return best

def results_output(num_of_cell, test_no, fleet, cell_num):
    output = open('vrp_output'+str(cell_num)+'.txt', 'a')
    output.write('('+str(num_of_cell)+','+str(test_no)+')')
    max_service = max(i.service_time for i in fleet)
    min_service = min(i.service_time for i in fleet)
    tot_service = sum(i.service_time for i in fleet)
    ratio = float(max_service)/min_service
    output.write('{MaxServiceTime: %s, MinServiceTime: %s, Ratio: %s, Tot_time: %s}' % (str(max_service), str(min_service), str(ratio), str(tot_service)))
    output.write('\n')

    output.close()


for cell_num in range(80, 90, 5):
    state = True
    test_tot = 20
    with open('processes.txt', 'a') as f:
        f.writelines('Num of cells'+str(cell_num))
    # for i in range(1, test_tot):
    for i in range(1, 16):
        state = True
        numVehicle = 5
        while state:
            try:
                with open('processes.txt', 'a') as f:
                    f.writelines('solve'+str(i)+'\n')
                all_cell = read_cells(cell_num, i)
                # points, maxIteration, maxTabu, numVehicle, maxCandidate, maxCapacity
                final_solution = search(all_cell, 50, 5, numVehicle, 1000, 1000)
                results_output(cell_num, i, final_solution.fleet, cell_num)
                state = False
            except GurobiError:
                numVehicle -= 1
                if numVehicle <= 1:
                    state = False
                    with open('processes.txt', 'a') as f:
                        f.writelines('Num of cells'+str(cell_num)+'No Solution!\n')
            print 'NUM of Vehicle '+str(numVehicle)
