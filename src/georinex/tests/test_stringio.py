import importlib.resources as ir
import pytest
from pytest import approx

import io
from datetime import datetime

import georinex as gr


@pytest.mark.parametrize(
    "rinex_version, t", [(2, datetime(1999, 9, 2, 19)), (3, datetime(2010, 10, 18, 0, 1, 4))]
)
def test_nav3(rinex_version, t):
    fn = ir.files(f"{__package__}.data") / f"minimal{rinex_version}.10n"
    txt = fn.read_text()

    with io.StringIO(txt) as f:
        info = gr.rinexinfo(f)
        assert info["rinextype"] == "nav"

        times = gr.gettime(f)
        nav = gr.load(f)

    assert times == t

    assert nav.equals(gr.load(fn)), "StringIO not matching direct file read"


@pytest.mark.parametrize("rinex_version", [2, 3])
def test_obs(rinex_version):
    fn = ir.files(f"{__package__}.data") / f"minimal{rinex_version}.10o"
    txt = fn.read_text()

    with io.StringIO(txt) as f:
        info = gr.rinexinfo(f)
        assert info["rinextype"] == "obs"

        times = gr.gettime(f)
        obs = gr.load(f)

    assert times == datetime(2010, 3, 5, 0, 0, 30)

    assert obs.equals(gr.load(fn)), "StringIO not matching direct file read"


def test_locs():
    gg = pytest.importorskip("georinex.geo")

    txt = (ir.files(f"{__package__}.data") / "demo.10o").read_text()

    with io.StringIO(txt) as f:
        locs = gg.get_locations(f)

    if locs.size == 0:
        pytest.skip("no locs found")

    assert locs.iloc[0].values == approx([41.3887, 2.112, 30])
