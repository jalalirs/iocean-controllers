# iocean controllers

Controllers for iocean vehicles, written against the iocean SDK, built and
deployed by the platform straight from this repository.

| controller | vehicle | what it does |
|---|---|---|
| `station-hold` | BlueROV2 | holds its position and depth against a current |
| `go-around-things` | BlueROV2 | goes to a goal and around what it meets on the way |
| `learned-hold` | BlueROV2 | a linear hold whose weights were learned in the tank (`train.py`) |
| `sawtooth` | Seaglider | dives and climbs on its buoyancy, the glider's sawtooth |

## Layout

```
iocean.toml                     the index: one [[controller]] per controller
controllers/<slug>/controller.py    the controller (a class built on iocean.Controller)
controllers/<slug>/requirements.txt its Python packages, if it needs any
tests/                          every listed controller checked and run in the tank
```

## Working on one

```bash
pip install -e ../auv/packages/sdk-python        # the SDK, from the iocean checkout
iocean tank controllers/station-hold/controller.py --task hold
python -m pytest tests                            # every controller, in the tank
```

## Deploying

In the iocean app: Controllers, Deploy one, From GitHub, this repository. The
platform clones it once, and for each controller here installs its packages,
checks it can fly its vehicle, runs it 20 s in the tank, puts it on the ROS 2
base and registers it, with the commit it came from. Pull latest rebuilds them
from the newest commit.
