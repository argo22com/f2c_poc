#!/bin/python

import fields2cover as f2c

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
    point = f2c.Point()
    point.importFromWkt("POINT (" + str(i[0]) + " " + str(i[1]) + " 0)")
    ring.addPoint(point)

print("Area of the ring space: ", ring.getArea())

f2c.Visualizer.plot(ring)
f2c.Visualizer.show()
f2c.Visualizer.save("/output/xxx-image")
