#!/bin/python

import fields2cover as f2c
from osgeo import ogr
from osgeo import osr
import math

def research():
    img_target = "/output/field_vis"

    def fn_robot():
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
        robot = fn_robot()
        ring = fn_ring(getBoundaries())
        field = fn_field(ring)
        field.setEPSGCoordSystem(32756)
        hl_ring = fn_ring(getHeadlandBoundaries())
        headland = f2c.Cells(f2c.Cell(hl_ring))
        swaths = fn_swaths(robot, headland)

        visualize(
                [field.getCellsAbsPosition().getCell(0), headland.getCell(0)],
                swaths)

        return [field.getArea(),
                headland.getArea(),
                img_target + '.png',
                ring.exportToJson(),
                hl_ring.exportToJson(),
                field.field.getGeometry(0).exportToJson(),
                field.isCoordSystemEPSG(),
                field.isCoordSystemUTM(),
                field.getCellsAbsPosition().getGeometry(0).exportToJson()
                ]

    def fn_swaths(robot, headland, algoImpl=None):
        if algoImpl == None:
            algoImpl = f2c.SG_BruteForce()
        swath = f2c.OBJ_SwathLength() # cost function
        return algoImpl.generateBestSwaths(
                swath,
                robot.op_width,
                headland.getGeometry(0))


    def fn_headland(field, robot):
        hl = f2c.HG_Const_gen();
        return hl.generateHeadlands(field.field, robot.robot_width)

    def fn_field(ring):
        cell = f2c.Cell(ring)
        cells = f2c.Cells(cell)
        field = f2c.Field(cells, "Plana test-field")
        return field

    def fn_ring(boundaries):
        ring = f2c.LinearRing()
        for i in boundaries:
            ring.addPoint(point(str(i[0]), str(i[1])))
        # add the first point again to close the circle
        ring.addPoint(point(str(boundaries[0][0]), str(boundaries[0][1])))
        return ring

    def visualize(cellItems, swaths):
        plotCellItems(cellItems)
        plotSwaths(swaths)
        f2c.Visualizer.show()
        f2c.Visualizer.save(img_target)

    def plotCellItems(cellItems):
        iter = 0
        for item in cellItems:
            f2c.Visualizer.plot(item, plotColour(iter))
            iter = iter + 1
        return iter

    def plotSwaths(swaths):
        mls = f2c.MultiLineString()
        for swath in swaths:
            ls = swath.getPath()
            mls.addGeometry(ls)
        f2c.Visualizer.plot(mls)

    def plotColour(intOrder):
        colours = ["brown", "gray", "green", "red", "purple", "blue", "pink",
                "orange", "olive", "cyan"]
        return "tab:{}".format(colours[intOrder % 10])

    def getBoundaries():
        return [[48.941325, 14.452474],
                [48.941347, 14.452458],
                [48.942325, 14.452615],
                [48.942313, 14.452802],
                [48.941827, 14.452680],
                [48.941791, 14.452698],
                [48.941324, 14.452555],
                [48.941322, 14.452484]]

    def getHeadlandBoundaries():
        return [[48.941394, 14.452505],
                [48.941400, 14.452466],
                [48.942137, 14.452581],
                [48.942132, 14.452745],
                [48.941827, 14.452680],
                [48.941791, 14.452698],
                [48.941384, 14.452573],
                [48.941392, 14.452516]]

    return run(img_target)
