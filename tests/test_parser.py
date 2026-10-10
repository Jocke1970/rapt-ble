import logging
import struct

import pytest
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import (
    DeviceKey,
    SensorDescription,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
)

from rapt_ble.custom_state_data import DeviceClass, Units
from rapt_ble.parser import (
    RAPTPillBluetoothDeviceData,
    RAPTTemperatureBluetoothDeviceData,
    decode_rapt_temperature,
)


@pytest.fixture(autouse=True)
def logging_config(caplog):
    caplog.set_level(logging.DEBUG)


def bytes_to_service_info(payload: bytes) -> BluetoothServiceInfo:
    manufacturer_data = {}
    (manufacturer_id,) = struct.unpack("<H", payload[:2])
    manufacturer_data[manufacturer_id] = payload[2:]

    return BluetoothServiceInfo(
        name="",
        address="00:11:22:33:44:55",
        rssi=-60,
        manufacturer_data=manufacturer_data,
        service_data={},
        service_uuids=[],
        source="local",
    )


@pytest.mark.parametrize(
    "data_bytes",
    [
        # payload v1
        b"RAPT\x01x\xe3m<\xb9\x94\x94\x8bD|\xb9\xf64E\x02b&w*\xac",
        # payload v2 - invalid gravity velocity
        b"RAPT\x02\x00\x00\x00\x00\x00\x00\x94\x8bD|\xb9\xf64E\x02b&w*\xac",
        # payload v2 - valid gravity velocity
        b"RAPT\x02\x00\x01\xc1\x6d\x26\x14\x92\x6b\x44\x7f\x52\xc9\x31\xc9\x02\x2d\x29\x97\x3f\x46",
        b"RAPTdPillG1",
        b"KEG20220612_050156_81c6d1",
    ],
)
def test_device_supported(data_bytes):
    device = RAPTPillBluetoothDeviceData()

    data = bytes_to_service_info(data_bytes)

    assert device.supported(data)


def test_parse_version():
    device = RAPTPillBluetoothDeviceData()
    data = bytes_to_service_info(b"KEG20220612_050156_81c6d1")
    device.update(data)
    assert device._get_device_info(None).sw_version == "20220612_050156_81c6d1"


def test_parse_metrics_v1():
    device = RAPTPillBluetoothDeviceData()
    data = bytes_to_service_info(
        b"RAPT\x01x\xe3m<\xb9\x94\x94\x8bD|\xb9\xf64E\x02b&w*\xac"
    )
    result = device.update(data)
    assert result == SensorUpdate(
        title="RAPT Pill 4455",
        devices={
            None: SensorDeviceInfo(
                name="RAPT Pill 4455",
                manufacturer="RAPT",
                model="RAPT Pill hydrometer",
                hw_version=None,
                sw_version=None,
            ),
        },
        entity_descriptions={
            DeviceKey(key="specific_gravity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="specific_gravity", device_id=None): SensorValue(
                device_key=DeviceKey("specific_gravity", device_id=None),
                name="Specific Gravity",
                native_value=1.0109,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=23.94,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=43,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-60,
            ),
        },
    )


def test_parse_metrics_v2():
    device = RAPTPillBluetoothDeviceData()
    data = bytes_to_service_info(
        b"RAPT\x02\x00\x01\xc1\x6d\x26\x14\x92\x6b\x44\x7f\x52\xc9\x31\xc9\x02\x2d\x29\x97\x3f\x46",
    )
    result = device.update(data)
    assert result == SensorUpdate(
        title="RAPT Pill 4455",
        devices={
            None: SensorDeviceInfo(
                name="RAPT Pill 4455",
                manufacturer="RAPT",
                model="RAPT Pill hydrometer",
                hw_version=None,
                sw_version=None,
            ),
        },
        entity_descriptions={
            DeviceKey(key="specific_gravity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(
                key="specific_gravity_velocity", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="specific_gravity_velocity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY_VELOCITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY_POINTS_PER_DAY,
            ),
        },
        entity_values={
            DeviceKey(key="specific_gravity", device_id=None): SensorValue(
                device_key=DeviceKey("specific_gravity", device_id=None),
                name="Specific Gravity",
                native_value=1.0213,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=19.69,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=63,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-60,
            ),
            DeviceKey(key="specific_gravity_velocity", device_id=None): SensorValue(
                device_key=DeviceKey("specific_gravity_velocity", device_id=None),
                name="Specific Gravity Velocity",
                native_value=-14.821796417236328,
            ),
        },
    )


def test_parse_metrics_v2_no_velocity():
    device = RAPTPillBluetoothDeviceData()
    data = bytes_to_service_info(
        b"RAPT\x02\x00\x00\x00\x00\x00\x00\x94\x8bD|\xb9\xf64E\x02b&w*\xac",
    )
    result = device.update(data)
    assert result == SensorUpdate(
        title="RAPT Pill 4455",
        devices={
            None: SensorDeviceInfo(
                name="RAPT Pill 4455",
                manufacturer="RAPT",
                model="RAPT Pill hydrometer",
                hw_version=None,
                sw_version=None,
            ),
        },
        entity_descriptions={
            DeviceKey(key="specific_gravity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(
                key="specific_gravity_velocity", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="specific_gravity_velocity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY_VELOCITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY_POINTS_PER_DAY,
            ),
        },
        entity_values={
            DeviceKey(key="specific_gravity", device_id=None): SensorValue(
                device_key=DeviceKey("specific_gravity", device_id=None),
                name="Specific Gravity",
                native_value=1.0109,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=23.94,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=43,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-60,
            ),
            DeviceKey(key="specific_gravity_velocity", device_id=None): SensorValue(
                device_key=DeviceKey("specific_gravity_velocity", device_id=None),
                name="Specific Gravity Velocity",
                native_value=None,
            ),
        },
    )


RAPT_TEMP_UUID = bytes.fromhex("4b6567b722314977852625b74c616e64")


def rapt_temp_service_info(
    raw_temperature: int, battery: int = 67, minor_low: int = 0
) -> BluetoothServiceInfo:
    """Build a service info object matching a captured RAPT Temp iBeacon packet."""
    payload = (
        bytes.fromhex("4c00")
        + bytes.fromhex("0215")
        + RAPT_TEMP_UUID
        + struct.pack(">H", raw_temperature)
        + bytes([battery, minor_low])
        + bytes.fromhex("00")
    )
    return bytes_to_service_info(payload)


def test_decode_rapt_temperature():
    # Captured at approximately 33.6 C: 0x4CAA = 19626.
    assert decode_rapt_temperature(0x4CAA) == 33.51
    # Captured during the warm-up run near 43.1 C: 0x4F10 = 20240.
    assert decode_rapt_temperature(0x4F10) == 43.1


def test_rapt_temperature_device_supported():
    device = RAPTTemperatureBluetoothDeviceData()
    assert device.supported(rapt_temp_service_info(0x4CAA))


def test_parse_rapt_temperature():
    device = RAPTTemperatureBluetoothDeviceData()
    result = device.update(rapt_temp_service_info(0x4CAA))

    assert result == SensorUpdate(
        title="RAPT Temp 4455",
        devices={
            None: SensorDeviceInfo(
                name="RAPT Temp 4455",
                manufacturer="RAPT",
                model="RAPT Bluetooth Thermometer",
                hw_version=None,
                sw_version=None,
            ),
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="debug_minor_lo", device_id=None): SensorDescription(
                device_key=DeviceKey(key="debug_minor_lo", device_id=None),
                device_class=DeviceClass.DEBUG,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=33.51,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=67,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-60,
            ),
            DeviceKey(key="debug_minor_lo", device_id=None): SensorValue(
                device_key=DeviceKey(key="debug_minor_lo", device_id=None),
                name="Debug Minor Low Byte",
                native_value=0,
            ),
        },
    )


def test_rapt_temperature_battery_percentage():
    device = RAPTTemperatureBluetoothDeviceData()
    result = device.update(rapt_temp_service_info(0x4CAA, battery=64))

    assert result is not None
    assert result.entity_values[
        DeviceKey(key="battery", device_id=None)
    ].native_value == 64


def test_rapt_temperature_rejects_other_ibeacon_uuid():
    device = RAPTTemperatureBluetoothDeviceData()
    data = rapt_temp_service_info(0x4CAA)
    data.manufacturer_data[76] = (
        bytes.fromhex("0215")
        + bytes.fromhex("00112233445566778899aabbccddeeff")
        + bytes.fromhex("4caa430000")
    )
    assert not device.supported(data)
