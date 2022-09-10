"""Support for sensor value(s) stored in a remote url."""
import os
import logging
import requests

import aiohttp
from aiohttp import hdrs
import async_timeout

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_VALUE_TEMPLATE, CONF_NAME, CONF_UNIT_OF_MEASUREMENT)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_URL = 'url'

DEFAULT_NAME = 'Url`'
DEFAULT_TIMEOUT = 10
DEFAULT_METHOD = 'get'
DEFAULT_VERIFY_SSL = True

SUPPORT_HTTP_METHODS = [
    'get'
]

ICON = 'mdi:file'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
})

# see https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/rest_command/__init__.py

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up the url sensor."""
    url = config.get(CONF_FILE_PATH)
    name = config.get(CONF_NAME)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)
    value_template = config.get(CONF_VALUE_TEMPLATE)

#    auth = None
#    if CONF_USERNAME in command_config:
#        username = command_config[CONF_USERNAME]
#        password = command_config.get(CONF_PASSWORD, '')
#        auth = aiohttp.BasicAuth(username, password=password)

#    headers = None
#    if CONF_HEADERS in command_config:
#        headers = command_config[CONF_HEADERS]


    if value_template is not None:
        value_template.hass = hass

class UrlSensor(Entity):
    """Implementation of a url sensor."""

    def __init__(self, name, url, unit_of_measurement, value_template):
        """Initialize the url sensor."""
        self._name = name
        self._url = url
        self._unit_of_measurement = unit_of_measurement
        self._val_tpl = value_template
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Get the latest entry from a url and updates the state."""
        try:
            u = requests.get(self._url, stream=True)

            with async_timeout.timeout(timeout):
                    request = await getattr(websession, method)(
                        template_url.async_render(variables=service.data),
                        data=payload,
                        auth=auth,
                        headers=headers
                    )


            # FIXME
            with open(self._file_path, 'r', encoding='utf-8') as file_data:
                for line in file_data:
                    data = line
                data = data.strip()

        except (IndexError, FileNotFoundError, IsADirectoryError,
                UnboundLocalError):
            _LOGGER.warning("Url not available at the moment: %s",
                            os.path.basename(self._file_path))
            return

        if self._val_tpl is not None:
            self._state = self._val_tpl.async_render_with_possible_json_value(
                data, None)
        else:
            self._state = data
