"""Every controller listed in iocean.toml: it loads, it can fly the vehicle it
was written for, and it runs in the SDK's tank without raising."""

from __future__ import annotations

import pathlib
import tomllib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LISTED = tomllib.loads((ROOT / "iocean.toml").read_text())["controller"]


@pytest.mark.parametrize("entry", LISTED, ids=[c["slug"] for c in LISTED])
def test_it_can_fly_its_vehicle(entry):
    from iocean.loading import controller_from

    file, _, name = entry["entry"].partition(":")
    cls = controller_from(f"{ROOT / file}:{name}")
    problems = cls().described.check(cls)
    assert problems == [], problems


@pytest.mark.parametrize("entry", LISTED, ids=[c["slug"] for c in LISTED])
def test_it_runs_in_the_tank(entry):
    from iocean.loading import controller_from
    try:
        from iocean.tank import Tank, _runtime
        _runtime()
    except ImportError:
        pytest.skip("the tank needs the iocean runtime (IOCEAN_RUNTIME)")

    file, _, name = entry["entry"].partition(":")
    cls = controller_from(f"{ROOT / file}:{name}")
    report = Tank(cls.vehicle, seconds=10.0).run(cls())
    assert report.seconds >= 9.9
