"""
test for LZW .Z file
"""

import importlib.resources as ir
import pytest

import georinex as gr


def test_obs2_lzw():
    pytest.importorskip("ncompress")

    fn = ir.files(f"{__package__}.data") / "ac660270.18o.Z"

    obs = gr.load(fn)

    hdr = gr.rinexheader(fn)

    assert hdr["t0"] <= gr.to_datetime(obs.time[0])

    assert not obs.fast_processing
