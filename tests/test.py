from netcdf2geotiff import rgb_geotiff, singleband_geotiff

rgb_geotiff("test.nc", "test.tif", "RED", "GREEN", "BLUE", "lat", "lon")

singleband_geotiff("test.nc", "test.tif", "IDEPIX_SNOW_ICE", "lat", "lon")