# RAPT Bluetooth Thermometer protocol notes

These notes document the current reverse-engineering status of the RAPT
Bluetooth Thermometer BLE advertisement used by this fork.

The goal is to keep verified protocol knowledge separate from temporary test
instrumentation so the eventual upstream contribution can remain small and
well-supported.

## Advertisement format

The thermometer advertises as an Apple iBeacon using manufacturer ID
`0x004c` (decimal `76`).

The iBeacon UUID observed on the physical thermometer is:

`4b6567b7-2231-4977-8526-25b74c616e64`

The manufacturer payload after the manufacturer ID is 23 bytes:

| Offset | Length | iBeacon field | RAPT interpretation | Status |
| --- | ---: | --- | --- | --- |
| 0-1 | 2 | Header | `02 15` | Verified |
| 2-17 | 16 | UUID | RAPT thermometer UUID | Verified |
| 18-19 | 2 | Major | Temperature raw value | Verified |
| 20 | 1 | Minor high byte | Battery percentage | Verified |
| 21 | 1 | Minor low byte | Unknown / reserved | Unknown |
| 22 | 1 | TX power | Standard iBeacon field | Observed as `0` |

All multi-byte iBeacon major/minor values are read big-endian.

## Temperature

The iBeacon `major` field contains temperature as fixed-point Kelvin:

```text
temperature_c = raw_major / 64 - 273.15
```

Examples observed during hardware testing:

| Raw major | Decoded temperature |
| ---: | ---: |
| 19274 | 28.01 °C |
| 19600 | 33.10 °C |
| 19606 | 33.19 °C |
| 19613 | 33.30 °C |
| 19619 | 33.40 °C |

The decoded values track the Home Assistant temperature sensor and physical
temperature changes as expected.

## Battery

The high byte of the iBeacon `minor` field is interpreted as an integer
battery percentage.

Observed values during live testing include:

- `0x43` = 67%
- `0x42` = 66%
- `0x40` = 64%

During this period the physical thermometer displayed two of three battery
bars. The advertised value also changed over time while the low byte remained
zero.

This behaviour, combined with the direct percentage-like range, is considered
sufficiently strong to expose the high byte as a normal battery percentage
sensor.

## Minor low byte

The low byte of the iBeacon `minor` field has so far remained:

`0x00`

No reliable relationship has been found between this byte and temperature,
battery level, RSSI or the visible device state.

For now it is exposed only as the temporary diagnostic sensor
`Debug Minor Low Byte`.

Before the upstream pull request one of two things should happen:

1. identify and document a reproducible meaning for the byte, or
2. remove the diagnostic sensor and leave the byte ignored.

The upstream contribution should not expose an unknown protocol field as a
normal sensor.

## TX power

The final iBeacon byte has been observed as `0` in the captured packets.

It is currently logged for reverse-engineering purposes but is not exposed as a
sensor because it is not needed for the thermometer feature.

## Upstream PR scope

The intended upstream parser contribution should include only:

- RAPT thermometer iBeacon discovery / matching
- temperature decoding
- battery percentage decoding
- regression tests based on captured advertisements
- no behavioural changes to existing RAPT Pill support

The temporary Home Assistant / HACS wrapper used by this fork for hardware
validation is intentionally separate from the parser feature and should not be
part of the upstream library pull request.
