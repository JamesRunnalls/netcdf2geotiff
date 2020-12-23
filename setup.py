from setuptools import setup, find_packages

setup(
    name='netcdf2geotiff',
    version='0.1',
    description='Convert NetCDF file to Geotiff',
    download_url="https://github.com/JamesRunnalls/netcdf2geotiff",
    author='James Runnalls',
    licens ="MIT",
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        "netCDF4",
        "GDAL",
    ],
)
