import importlib.resources as ir

import pytest

import georinex as gr


@pytest.mark.parametrize(
    "fn, rtype, vers",
    [
        ("minimal2.10o", "obs", 2.11),
        ("minimal3.10o", "obs", 3.01),
        ("minimal2.10n", "nav", 2.11),
        ("minimal3.10n", "nav", 3.01),
        ("york0440.15d", "obs", 1.00),
        ("r2all.nc", "obs", 2.11),
    ],
    ids=["obs2", "obs3", "nav2", "nav3", "Cobs1", "NetCDF_obs2"],
)
def test_header(fn, rtype, vers):
    fn = ir.files(f"{__package__}.data") / fn
    if fn.suffix == ".nc":
        pytest.importorskip("netCDF4")

    hdr = gr.rinexheader(fn)
    assert isinstance(hdr, dict)
    assert rtype in hdr["rinextype"]
    assert hdr["version"] == pytest.approx(vers)

    # make sure string filenames work too
    hdr = gr.rinexheader(str(fn))
    assert isinstance(hdr, dict)


@pytest.mark.parametrize(
    "fn",
    ["demo.10o", "demo3.10o"],
    ids=["obs2", "obs3"],
)
def test_position(fn):
    hdr = gr.rinexheader(ir.files(f"{__package__}.data") / fn)
    assert len(hdr["position"]) == 3
