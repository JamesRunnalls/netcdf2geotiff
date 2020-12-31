from netcdf2geotiff import rgb_geotiff, singleband_geotiff

rgb_geotiff("test3.nc", "test3.tif", "RED", "GREEN", "BLUE", "lat", "lon")

singleband_geotiff("test3.nc", "tests3.tif", "IDEPIX_SNOW_ICE", "lat", "lon")