#!/usr/bin/env python
from osgeo import gdal
from osgeo import osr
import numpy as np
import os, sys
from netCDF4 import Dataset
osr.UseExceptions()

def rgb_geotiff(file, outfile, red, green, blue, lat, lon):
    with Dataset(file, "r", format="NETCDF4") as nc:
        red = np.array(nc.variables[red][:])
        green = np.array(nc.variables[green][:])
        blue = np.array(nc.variables[blue][:])
        lat = np.array(nc.variables[lat][:])
        lon = np.array(nc.variables[lon][:])
        image_size = red.shape

    r_pixels = np.around((( red - np.amin(red) ) / ( np.amax(red) - np.amin(red) )) * 255)
    g_pixels = np.around((( green - np.amin(green) ) / ( np.amax(green)  - np.amin(green) )) * 255)
    b_pixels = np.around((( blue - np.amin(blue) ) / ( np.amax(blue)  - np.amin(blue) )) * 255)

    # set geotransform
    nx = image_size[0]
    ny = image_size[1]
    xmin, ymin, xmax, ymax = [min(lon), min(lat), max(lon), max(lat)]
    xres = (xmax - xmin) / float(ny)
    yres = (ymax - ymin) / float(nx)
    geotransform = (xmin, xres, 0, ymax, 0, -yres)

    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create(outfile, ny, nx, 3, gdal.GDT_Byte)

    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(4326)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(r_pixels)   # write r-band to the raster
    dst_ds.GetRasterBand(2).WriteArray(g_pixels)   # write g-band to the raster
    dst_ds.GetRasterBand(3).WriteArray(b_pixels)   # write b-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None


def singleband_geotiff(file, outfile, band, lat, lon):
    with Dataset(file, "r", format="NETCDF4") as nc:
        band = np.array(nc.variables[band][:])
        lat = np.array(nc.variables[lat][:])
        lon = np.array(nc.variables[lon][:])
        image_size = band.shape

    b_pixels = np.around(((band - np.amin(band)) / (np.amax(band) - np.amin(band))) * 255)
    a_pixels = band

    # set geotransform
    nx = image_size[0]
    ny = image_size[1]
    xmin, ymin, xmax, ymax = [np.amin(lon), np.amin(lat), np.amax(lon), np.amax(lat)]
    xres = (xmax - xmin) / float(ny)
    yres = (ymax - ymin) / float(nx)
    geotransform = (xmin, xres, 0, ymax, 0, -yres)

    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create(outfile, ny, nx, 4, gdal.GDT_Byte)

    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(b_pixels)
    dst_ds.GetRasterBand(2).WriteArray(b_pixels)
    dst_ds.GetRasterBand(3).WriteArray(b_pixels)
    dst_ds.GetRasterBand(4).WriteArray(a_pixels)
    dst_ds.FlushCache()
    dst_ds = None

