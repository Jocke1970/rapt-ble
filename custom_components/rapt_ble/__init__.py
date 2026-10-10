"""Temporary RAPT Bluetooth test override for Home Assistant."""

import logging
from collections.abc import Callable

from home_assistant_bluetooth import BluetoothServiceInfo

from homeassistant.components.bluetooth import BluetoothScanningMode
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from rapt_ble import (
    RAPTPillBluetoothDeviceData,
    RAPTTemperatureBluetoothDeviceData,
    SensorUpdate,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type RAPTBLEConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


def _combined_update_method() -> Callable[[BluetoothServiceInfo], SensorUpdate | None]:
    """Return an update method supporting both RAPT Pill and RAPT Thermometer."""
    pill = RAPTPillBluetoothDeviceData()
    thermometer = RAPTTemperatureBluetoothDeviceData()

    def _update(service_info: BluetoothServiceInfo) -> SensorUpdate | None:
        if thermometer.supported(service_info):
            return thermometer.update(service_info)
        if pill.supported(service_info):
            return pill.update(service_info)
        return None

    return _update


async def async_setup_entry(hass: HomeAssistant, entry: RAPTBLEConfigEntry) -> bool:
    """Set up RAPT BLE device from a config entry."""
    address = entry.unique_id
    if address is None:
        raise RuntimeError("RAPT BLE config entry is missing a unique ID")

    coordinator = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.ACTIVE,
        update_method=_combined_update_method(),
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(coordinator.async_start())
    return True


async def async_unload_entry(hass: HomeAssistant, entry: RAPTBLEConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
