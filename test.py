#!/bin/python

import fields2cover as f2c
from osgeo import ogr

def robot():
    r = f2c.Robot(2.357, 2.357)
    r.cruise_speed = 0.5
    r.linear_curv_change = 1.0
    #r.max_vel = 1.0
    r.setMinRadius(3.0)
    return r

def point(lat, lon):
    ogrpoint = ogr.Geometry(ogr.wkbPoint)
    ogrpoint.AddPoint(float(lat), float(lon))
    point = f2c.Point()
    point.importFromWkt(ogrpoint.ExportToWkt())
    return point

boundaries = [
        [48.941325, 14.452474],
        [48.941347, 14.452458],
        [48.942325, 14.452615],
        [48.942313, 14.452802],
        [48.941827, 14.452680],
        [48.941791, 14.452698],
        [48.941324, 14.452555],
        [48.941322, 14.452484]]

ring = f2c.LinearRing()
for i in boundaries:
    ring.addPoint(point(str(i[0]), str(i[1])))
# add the first point again to close the circle
ring.addPoint(point(str(boundaries[0][0]), str(boundaries[0][1])))

cell = f2c.Cell(ring)
cells = f2c.Cells(cell)
field = f2c.Field(cells, "Test-field")

robot = robot()
const_hl = f2c.HG_Const_gen();
#no_hl = const_hl.generateHeadlands(cells, 3.0 * robot.robot_width)
no_hl = const_hl.generateHeadlands(cells, 0.000008)

print("Area of the field space: ", field.getArea())
print("Area of the field w/o headlands: ", no_hl.getArea())
#f2c.Visualizer.figure(100)
f2c.Visualizer.plot(cell, "tab:orange")
f2c.Visualizer.plot(no_hl.getCell(0))
f2c.Visualizer.show()
f2c.Visualizer.save("/output/field_new")
