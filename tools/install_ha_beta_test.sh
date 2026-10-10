#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${CONFIG_DIR:-/config}"
TARGET="${CONFIG_DIR}/custom_components/rapt_ble"
BASE_URL="https://raw.githubusercontent.com/Jocke1970/rapt-ble/ha-beta-debug-test-20261010/ha_test/custom_components/rapt_ble"

FILES=(
  "__init__.py"
  "config_flow.py"
  "const.py"
  "icons.json"
  "manifest.json"
  "sensor.py"
  "strings.json"
)

mkdir -p "${CONFIG_DIR}/custom_components"

if [ -d "${TARGET}" ]; then
  BACKUP="${TARGET}.bak_$(date +%Y%m%d_%H%M%S)"
  cp -a "${TARGET}" "${BACKUP}"
  echo "Existing override backed up to: ${BACKUP}"
fi

rm -rf "${TARGET}"
mkdir -p "${TARGET}"

for file in "${FILES[@]}"; do
  echo "Downloading ${file}..."
  curl -fL --retry 3 --connect-timeout 10     "${BASE_URL}/${file}"     -o "${TARGET}/${file}"
done

echo
echo "Installed temporary RAPT BLE test override:"
echo "  ${TARGET}"
echo
echo "Pinned parser commit:"
echo "  4ba24f09f03045f65d8b96bbecddfbe3e0a97bc9"
echo
echo "Restart Home Assistant Core to activate it:"
echo "  ha core restart"
echo
echo "After restart, check Settings -> Devices & services -> RAPT Bluetooth."
