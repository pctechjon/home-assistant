"""WLED Light integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    Light,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_EFFECT,
)

from homeassistant.const import CONF_HOST

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_HOST): cv.string})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the WLED Light platform."""
    from wledpy import wledpy

    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]

    controller = wledpy.wled.Wled(host)

    # Verify controller is responsive
    if not controller.is_valid():
        _LOGGER.error("Could not connect to WLED controller")
        return

    # Add devices
    add_entities(Wled(controller))


class Wled(Light):
    """Representation of a WLED light controller."""

    def __init__(self, light):
        """Initialize a WLED controller."""
        self._light = light
        self._name = light.name
        self._state = light.state
        self._brightness = light.brightness
        self._color = light.color
        self._effect = light.effect

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""

        self._light.brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._light.turn_on()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.turn_off()

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def effect(self):
        """Return the current effect of the light."""
        return self._effect

    def update(self):
        """Fetch new state data for this light."""
        wled_state = self._light.update()
        self._name = wled_state.name
        self._state = wled_state.state
        self._brightness = wled_state.brightness
        self._color = wled_state.color
        self._effect = wled_state.effect
        self._transition = wled_state.transition

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR | SUPPORT_EFFECT
