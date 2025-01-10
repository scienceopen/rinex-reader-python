"""
Self-test file, registration case
for OBS RINEX reader
"""

import importlib.resources as ir

from datetime import datetime

import xarray
import pytest
from pytest import approx

import georinex as gr


@pytest.mark.parametrize(
    "time, exp_time",
    [
        (None, None),
        (datetime(2019, 1, 1), datetime(2019, 1, 1)),
        (xarray.DataArray(datetime(2019, 1, 1)), datetime(2019, 1, 1)),
    ],
)
def test_to_datetime(time, exp_time):
    assert gr.to_datetime(time) == exp_time


def test_bad_files(tmp_path):
    emptyfn = tmp_path / "nonexistingfilename"
    emptyfn.touch()
    emptyfnrinex = tmp_path / "nonexistingfilename.18o"
    emptyfnrinex.touch()
    emptyfnNC = tmp_path / "nonexistingfilename.nc"
    emptyfnNC.touch()

    nonexist = tmp_path / "nonexist"  # don't touch

    with pytest.raises(ValueError):
        gr.load(emptyfn)

    with pytest.raises(ValueError):
        gr.load(emptyfnrinex)

    with pytest.raises(FileNotFoundError):
        gr.load(nonexist)

    with pytest.raises(ValueError):
        gr.load(emptyfnNC)


def test_netcdf_read():
    pytest.importorskip("netCDF4")

    dat = gr.load(ir.files(f"{__package__}.data") / "r2all.nc")

    assert isinstance(dat, dict), f"{type(dat)}"
    assert isinstance(dat["obs"], xarray.Dataset)


def test_netcdf_write(tmp_path):
    """
    NetCDF4 wants suffix .nc -- arbitrary tempfile.NamedTemporaryFile names do NOT work!
    """
    pytest.importorskip("netCDF4")

    fn = tmp_path / "rw.nc"
    obs = gr.load(ir.files(f"{__package__}.data") / "demo.10o", out=fn)

    wobs = gr.load(fn)

    assert obs.equals(wobs)


def test_netcdf_write_sp3(tmp_path):
    """
    NetCDF4 wants suffix .nc -- arbitrary tempfile.NamedTemporaryFile names do NOT work!
    """
    pytest.importorskip("netCDF4")

    fn = tmp_path / "sp3.nc"
    obs = gr.load(ir.files(f"{__package__}.data") / "example1.sp3a", out=fn)

    wobs = xarray.load_dataset(fn)

    assert obs.equals(wobs)

    assert obs.attrs == wobs.attrs


def test_locs():
    pytest.importorskip("pymap3d")  # need to have this
    gg = pytest.importorskip("georinex.geo")

    pat = ["*o", "*O.rnx", "*O.rnx.gz", "*O.crx", "*O.crx.gz"]

    flist = gr.globber(ir.files(f"{__package__}.data"), pat)

    locs = gg.get_locations(flist)

    assert locs.loc["demo.10o"].values == approx([41.3887, 2.112, 30])


@pytest.mark.parametrize("dtype", ["OBS", "NAV"])
def test_nc_load(dtype):
    pytest.importorskip("netCDF4")

    truth = xarray.open_dataset(ir.files(f"{__package__}.data") / "r2all.nc", group=dtype)

    obs = gr.load(ir.files(f"{__package__}.data") / f"demo.10{dtype[0].lower()}")
    assert obs.equals(truth)
