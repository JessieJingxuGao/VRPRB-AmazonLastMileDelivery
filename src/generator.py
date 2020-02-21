# coding = utf-8
# __author__ = ''


'''
Function: generate random cell data for VRP
'''

import random
import io
import xlwt
import math
import utilities


class Cell:

    def __init__(self, longitude, latitude, customer_orders):
        self.lng = longitude
        self.lat = latitude
        self.orders = customer_orders


class Dot:

    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy

def cell_generator(num, repeat):

    no = u'No.'
    longitude = u'Longitude'
    latitude = u'Latitude'
    order = u'orders'
    with io.open(u'tester_cell_large_scale/CellSource_'+unicode(num)+u'_'+unicode(repeat)+u'.txt', 'w') as cfile:
        cfile.write(no+u' '+longitude+u' '+latitude+u' '+order+'\n')
        for i in range(num):
            if i == 0:
                cells = Cell(50, 50, int(random.uniform(3, 40)))
            else:
                random.seed()
                # currently using uniform dist. to get number of orders
                cells = Cell(round(random.random()*100, 3), round(random.random()*100, 3), int(random.uniform(2, 40)))

            cfile.write(unicode(i+1)+u' ')
            cfile.write(unicode(cells.lng)+u' ')
            cfile.write(unicode(cells.lat)+u' ')
            cfile.write(unicode(cells.orders)+u' ')
            cfile.write(u'\n')
        cfile.close()

# get cells in txt
'''for i in range(80, 152, 5):
    for j in range(1, 21):
        cell_generator(i, j)
'''


def cell_excel(a, b, num, rand_id):
    title = [u'No.', u'Longitude', u'Latitude', u'orders', u'dist_in_cell']
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(u'cells')
    for i in range(5):
        sheet.write(0, i, title[i])


    for i in range(num):
        if i == 0:
            cells = Cell(50, 50, int(random.uniform(3, 40)))
        else:
            random.seed()
            # currently using uniform dist. to get number of orders
            cells = Cell(round(random.random()*100, 3), round(random.random()*100, 3), int(random.uniform(2, 40)))

        sheet.write(i+1, 0, i+1)
        sheet.write(i+1, 1, cells.lng)
        sheet.write(i+1, 2, cells.lat)
        sheet.write(i+1, 3, cells.orders)


    workbook.save(u'Oval_'+unicode(num)+u'_'+unicode(rand_id)+u'.xls')

'''       if cells.orders < 12:
            x = cells.orders/4
            phi = 2/float(x*x)*float((1+x)*math.log(1+x, math.e)-x)
            dist = cells.orders*(100/6+2*phi/(float(cells.orders)/100))
        else:
            dist = 0.9*math.sqrt(cells.orders*100*100)
        sheet.write(i+1, 4, dist)
'''

# get cells in txt
'''for i in range(10, 36, 5):
    for j in range(1, 31):
        cell_excel(1, 1, i, j)
'''

# get random cells located in oval


# a and b are parameters of the oval
# num stands for the number of points you would like to generate in the oval
# repeat is actually the id of a sample
def oval_order_generator(a, b, num, repeat):

    title = [u'No.', u'x-axis', u'y-axis']
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(u'cells')
    dots = []
    for i in range(3):
        sheet.write(0, i, title[i])
    for i in range(num):
        random.seed()
        # currently using uniform dist. to get number of orders
        xx = round(random.random()*2*a, 3)
        yy = 0.0
        while True:
            yy = round(random.random()*2*b, 3)
            if ((xx-a)*(xx-a)/(a*a)+(yy-b)*(yy-b)/(b*b)) < 1:
                break
        print xx, yy
        dots.append(Dot(xx, yy))
        sheet.write(i+1, 0, i+1)
        sheet.write(i+1, 1, xx)
        sheet.write(i+1, 2, yy)

    workbook.save(u'Oval_'+unicode(num)+u'_'+unicode(repeat)+u'.xls')
    return dots

for i in range(1):
    points = oval_order_generator(100, 50, 100, i+1)
    utilities.plot_points(points, 0, 200, 0, 100)
