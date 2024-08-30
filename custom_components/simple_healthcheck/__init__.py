from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TypedDict, cast
import voluptuous as vol

import homeassistant.core as ha
import homeassistant.helpers.config_validation as cv
from homeassistant.components import recorder
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import CoreState
from homeassistant.util import dt as dt_util


DOMAIN = "simple_healthcheck"

HEALTHCHECK_ENDPOINT = "/healthz"

EVENT_NAME = f"{DOMAIN}_event"
ENTITY_NAME = f"{DOMAIN}.last_seen"

_LOGGER: Final = logging.getLogger(__name__)

CONF_AUTH_REQUIRED = "auth_required"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_AUTH_REQUIRED, default=False): cv.boolean,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

class ConfData(TypedDict, total=False):

    auth_required: bool

async def async_setup(hass, config):
    conf: ConfData | None = config.get(DOMAIN)
    if conf is None:
        conf = cast(ConfData, CONFIG_SCHEMA({}))

    auth_required = conf.get(CONF_AUTH_REQUIRED)

    hass.data[DOMAIN] = {
        'auth_required': auth_required,
    }

    healthcheck_view = HealthCheckView(auth_required)
    hass.http.register_view(healthcheck_view)

    return True


class HealthCheckView(HomeAssistantView):
    url = HEALTHCHECK_ENDPOINT
    name = DOMAIN
    requires_auth = False

    def __init__(self, requires_auth):
        self.requires_auth = requires_auth

    @ha.callback
    def get(self, request):
        """ :type: HomeAssistant """
        hass: ha.HomeAssistant = request.app["hass"]

        if not hass.is_running:
            return self.json({"healthy": False}, HTTPStatus.SERVICE_UNAVAILABLE)

        recorder_instance = recorder.get_instance(hass)
        if not recorder_instance.async_recorder_ready.is_set() or not recorder_instance.migration_in_progress:
            return self.json({"healthy": False, "db": "Not ready"}, HTTPStatus.SERVICE_UNAVAILABLE)

        return self.json({"healthy": True})
