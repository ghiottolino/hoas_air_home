"""Platform for sensor integration."""
from __future__ import annotations
from datetime import timedelta
import logging
import async_timeout


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from homeassistant.const import POWER_WATT, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from ._airhome import AIRHOME


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Config entry example."""
    
    logging.info("initializing E3DC sensors with config:")
    logging.info(config)    
    
    COOKIE = config['cookie']
    SERIALNUMBER = str(config['serial_number'])

    airhome_api = AIRHOME(serialNumber = SERIALNUMBER, cookie= COOKIE)
    airhome_data = AirHomeData()
    
    async_add_entities(
        [VolumeFlowInput(airhome_api, airhome_data), ]
    )


class AirHomeData():
    """My custom coordinator."""

    def __init__(self):
        self.data = []

    def update(self,data):
        logging.info("Updating data with:")
        logging.info(data)
        self.data = data
    
    def get(self):
        logging.info("Reading data:")
        logging.info(self.data)
        return self.data

class AirHomeSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "AirHome Sensor"
    #_attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, api, e3dc_data):
        self.api = api
        self.airhome_api = airhome_api
        
    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        logging.info("Polling AirHome Web")
        airhome_status = self.api.poll()
        self.airhome_data.update(airhome_status)
        self._attr_native_value = airhome_status

class VolumeFlowInput(SensorEntity):
    _attr_name = "AirHome Volume Flow"
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, airhome_data):
        self.airhome_data = airhome_data
        
    def update(self) -> None:
        airhome_status = self.airhome_data.get()
        volumeflowinput = airhome_status['data'][0]['value']
        self._attr_native_value = volumeflowinput

class RoomTemperature(SensorEntity):
    _attr_name = "AirHome Room Temperature"
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, airhome_data):
        self.airhome_data = airhome_data

    def update(self) -> None:
        airhome_status = self.airhome_data.get()
        temproom = airhome_status['data'][1]['value']
        self._attr_native_value = temproom

class Humidiy(SensorEntity):
    _attr_name = "AirHome Humidiy"
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, airhome_data):
        self.airhome_data = airhome_data

    def update(self) -> None:
        airhome_status = self.airhome_data.get()
        humidityoutput = airhome_status['data'][2]['value']
        self._attr_native_value = humidityoutput

class HeatEmission(SensorEntity):
    _attr_name = "AirHome Heat Emission"
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, airhome_data):
        self.airhome_data = airhome_data

    def update(self) -> None:
        airhome_status = self.airhome_data.get()
        heat_emission = airhome_status['data'][4]['value']
        self._attr_native_value = heat_emission