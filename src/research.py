#!/bin/python

import fields2cover as f2c
from osgeo import ogr
from osgeo import osr

def research():
    global robot

    img_target = "/output/field_vis"

    def robot():
        r = f2c.Robot(2.357, 2.357)
        r.cruise_speed = 0.5
        r.linear_curv_change = 1.0
        #r.max_vel = 1.0
        r.setMinRadius(3.0)
        return r

    def point(lat, lon):
        point = f2c.Point()
        point.importFromWkt(ogrpoint(lat, lon).ExportToWkt())
        return point

    def ogrpoint(lat, lon):
        ogrpoint = ogr.Geometry(ogr.wkbPoint)
        ogrpoint.AddPoint(float(lat), float(lon))
        transformed = transform_by_epsg(ogrpoint)
        return transformed

    def transform_by_epsg(ogrpoint):
        in_sr = osr.SpatialReference()
        in_sr.ImportFromEPSG(4326) # standard WSG84
        out_sr = osr.SpatialReference()
        out_sr.ImportFromEPSG(32756) # WSG84 in meters
        ogrpoint.AssignSpatialReference(in_sr)
        ogrpoint.TransformTo(out_sr)
        return ogrpoint

    def run(img_target):
        # I don't get why this is necessary, but never mind
        global robot
        ring = f2c.LinearRing()
        boundaries = getBoundaries()
        for i in boundaries:
            ring.addPoint(point(str(i[0]), str(i[1])))
        # add the first point again to close the circle
        ring.addPoint(point(str(boundaries[0][0]), str(boundaries[0][1])))

        cell = f2c.Cell(ring)
        cells = f2c.Cells(cell)
        field = f2c.Field(cells, "Plana test-field")

        robot = robot()
        const_hl = f2c.HG_Const_gen();
        no_hl = const_hl.generateHeadlands(cells, robot.robot_width)

        visualize([cell, no_hl.getCell(0)])

        return [field.getArea(), no_hl.getArea(), img_target + '.png']

    def visualize(cellItems):
        f2c.Visualizer.figure(100)
        iter = 0
        for item in cellItems:
            f2c.Visualizer.plot(item, plotColour(iter))
            iter = iter + 1
        f2c.Visualizer.show()
        f2c.Visualizer.save(img_target)

    def plotColour(intOrder):
        if intOrder == 0:
            return "tab:orange"
        if intOrder == 1:
            return "tab:blue"
        # don't know more colours :(
        return "tab:olive"

    def getBoundaries():
        return [[48.941325, 14.452474],
                [48.941347, 14.452458],
                [48.942325, 14.452615],
                [48.942313, 14.452802],
                [48.941827, 14.452680],
                [48.941791, 14.452698],
                [48.941324, 14.452555],
                [48.941322, 14.452484]]

    return run(img_target)
