
# Pyvado

![Python Tests](https://github.com/AurelieSa/pyvado/actions/workflows/python-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-red?style=flat-square)

Python Vivado API

## Motivation

This project aims to provide a simple and as much comprehensive as possible tools for controlling vivado with python methods for vivado automation

## Structure

Pyvado is base on multiple manager, each runing a specific part of vivado. Manager are follows:
1. `TCLManager` : Basic manager for runing TCL command
2. `ProjectManager` : Vivado project manager
3. `FileManager` : Vivado file system manager
4. `FlowManager` : Vivado synthesis flow manager
5. `HardwareManager` : Vivado hardware manager
6. `ReportManager` : Vivado hardware report manager
7. `SimulatorManager` : Vivado simulation manager

These managers communicate to each other via `PyvadoSession` object and send TCL command directly to vivado process open in batch mode and controlled via `PyvadoProcess` class.

## Installation

```bash
pip install pyvado
```

## Usage

Basic synthesis flow annd hbitstream deploy usage
```py

# open Pyvado
with Pyvado("path/to/vivado/project.xpr") as pv:
  # open project
  pv.project.open()

  # add files
  pv.files.add_files("path/to/toplevel.vhd")
  pv.files.add_constraint_file("path/to/const.xdc")

  # run synthesis to bitstream
  pv.flow.set_toplevel("toplevel")
  pv.flow.run_all()

  # deploy bitstream to hardware
  pv.hardware.deploy()

```

Basic simulation
```py

# open Pyvado
with Pyvado("path/to/vivado/project.xpr") as pv:
  # open project
  pv.project.open()

  # add testbench
  pv.files.add_simulation_file("path/to/testbench.vhd")

  # open simulator
  pv.simulator.open()

  # run 80ns simulation
  pv.simulator.run("80ns")

```

Basic reports
```py

# open Pyvado
with Pyvado("path/to/vivado/project.xpr") as pv:
  # open project
  pv.project.open()

  # add files
  pv.files.add_files("path/to/toplevel.vhd")
  pv.files.add_constraint_file("path/to/const.xdc")

  # run synthesis to bitstream
  pv.flow.set_toplevel("toplevel")
  pv.flow.synhtesis()


  # open run
  pv.report.open("synth_1")
  pv.report.utilization("path/to/utilization.txt")
  pv.report.power("path/to/utilization.txt")

```

For more comprehensive tutorials, see example.


## Features

- [x] open vivado project
- [x] run TCL command lines
- [x] open vivado project
- [X] adding files
- [x] complete deployment workflow from synthesis to device programation
- [X] run behavioral simulation
- [X] generate report
- [X] vectorized simulation and vectorized power report
- [ ] create vivado project
- [ ] multiple vivado execution

## Roadmap

- comprehensive report manager
- create vivado project
- multiple vivado execution

## Contributing

Contribution are welcome.

## License

GPL v3 