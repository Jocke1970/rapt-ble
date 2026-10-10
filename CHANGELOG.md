# Changelog

<!--next-version-placeholder-->

## Unreleased

### Feature

* Add initial support for the RAPT Bluetooth Thermometer iBeacon advertisements.
* Decode thermometer temperature from fixed-point Kelvin and expose it in Celsius.
* Decode thermometer battery percentage from the high byte of the iBeacon minor field.
* Keep the low byte of the iBeacon minor field exposed as a temporary debug diagnostic while its meaning is still unknown.
* Document the verified thermometer payload layout and upstream cleanup plan.
* Add regression tests based on captured RAPT Bluetooth Thermometer advertisements.
* Preserve existing RAPT Pill parser behaviour.

## v0.1.2 (2023-06-16)

### Fix

* Fix condition, only show warning for payload >2 ([`453b065`](https://github.com/sairon/rapt-ble/commit/453b065171c93018d0c7b6a9111e21cfb3988606))

## v0.1.1 (2023-05-18)
### Fix
* Document v2 payload, remove warning ([`7bef92f`](https://github.com/sairon/rapt-ble/commit/7bef92fc3c1439a1d2c9180411aa695883c954a3))

## v0.1.0 (2023-02-10)
### Feature
* Initial implementation ([`1fa57bb`](https://github.com/sairon/rapt-ble/commit/1fa57bb31edd126ae2804fd20da65023aa7e4548))
