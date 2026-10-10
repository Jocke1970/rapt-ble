# RAPT BLE

<p align="center">
  <a href="https://github.com/sairon/rapt-ble/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/sairon/rapt-ble/ci.yml?branch=main&label=Upstream%20CI&logo=github&style=flat-square" alt="Upstream CI Status" >
  </a>
  <a href="https://rapt-ble.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/rapt-ble.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Upstream Documentation Status">
  </a>
  <a href="https://codecov.io/gh/sairon/rapt-ble">
    <img src="https://img.shields.io/codecov/c/github/sairon/rapt-ble.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Upstream test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square" alt="Poetry">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/rapt-ble/">
    <img src="https://img.shields.io/pypi/v/rapt-ble.svg?logo=python&logoColor=fff&style=flat-square" alt="Upstream PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/rapt-ble.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/rapt-ble.svg?style=flat-square" alt="License">
</p>

Python parser for RAPT BLE advertisements.

This fork extends the original [sairon/rapt-ble](https://github.com/sairon/rapt-ble)
library with support for the **RAPT Bluetooth Thermometer** while preserving the
existing **RAPT Pill hydrometer** support.

## Supported devices

### RAPT Pill

Existing upstream support for RAPT Pill BLE advertisements is unchanged.

### RAPT Bluetooth Thermometer

The thermometer parser currently:

- identifies the RAPT thermometer iBeacon UUID
  `4b6567b7-2231-4977-8526-25b74c616e64`
- decodes the advertised temperature
- exposes temperature in degrees Celsius
- decodes and exposes battery percentage
- exposes Bluetooth signal strength through the underlying Bluetooth data library
- ignores unrelated iBeacon UUIDs

The temperature payload is decoded from the iBeacon `major` field as a
fixed-point Kelvin value:

`temperature_c = raw_temperature / 64 - 273.15`

This decoding has been verified against captured advertisements from a physical
RAPT Bluetooth Thermometer and is covered by regression tests.

The battery percentage is carried in the high byte of the iBeacon `minor`
field. This has been validated against live hardware observations, including a
displayed two-of-three battery-bar state while the advertised value moved from
67% to 66% and then 64%.

The low byte of the `minor` field is still unknown. It has remained `0` in
the captures observed so far and is exposed only as a temporary diagnostic
during validation.

See [RAPT Bluetooth Thermometer protocol notes](docs/thermometer_protocol.md)
for the current byte map, evidence and upstream-readiness notes.

## Installation

The published `rapt-ble` package on PyPI is the upstream project. This fork is
currently intended for development and validation of the RAPT Bluetooth
Thermometer support and is **not published as a separate PyPI package**.

For the upstream package:

`pip install rapt-ble`

## Development status

RAPT Bluetooth Thermometer support is currently being validated before an
upstream contribution is proposed. The implementation lives on the normal
development path:

`dev -> beta -> main`

The known temperature and battery fields are considered decoded. The only
remaining reverse-engineering item is the low byte of the iBeacon `minor`
field. If no stable meaning can be identified, the temporary diagnostic sensor
will be removed before the upstream pull request so the contribution contains
only verified protocol fields.

## Upstream

Original project: [sairon/rapt-ble](https://github.com/sairon/rapt-ble)

The goal of this fork is to keep the implementation compatible with upstream
and suitable for a focused upstream pull request.

## Contributors ✨

Thanks goes to these wonderful people
([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the
[all-contributors](https://github.com/all-contributors/all-contributors)
specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
