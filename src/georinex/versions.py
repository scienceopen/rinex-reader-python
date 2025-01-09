import xarray
import numpy
import sys
import pandas

try:
    import netCDF4
except ImportError:
    pass

from . import __version__

print("Georinex", __version__)
print("Python", sys.version, sys.platform)
print("xarray", xarray.__version__)
print("Numpy", numpy.__version__)
print("Pandas", pandas.__version__)
try:
    print("NetCDF4", netCDF4.__version__)
except NameError:
    print("netCDF4 not available")

try:
    import pytest

    print("Pytest", pytest.__version__)
except ImportError:
    pass
