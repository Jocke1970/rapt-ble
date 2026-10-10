#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${CONFIG_DIR:-/config}"
TARGET="${CONFIG_DIR}/custom_components/rapt_ble"

if [ -d "${TARGET}" ]; then
  rm -rf "${TARGET}"
  echo "Removed temporary RAPT BLE custom override."
else
  echo "No temporary RAPT BLE override found."
fi

echo
echo "Restart Home Assistant Core to return to the built-in RAPT Bluetooth integration:"
echo "  ha core restart"
