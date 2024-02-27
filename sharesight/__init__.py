import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry
import voluptuous as vol

from .api import get_token, send_custom_price

DOMAIN = "sharesight"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    async def handle_send_price(call: ServiceCall):
        """Handle the service call to send price."""
        investment_id = call.data.get("investment_id")
        last_traded_price = call.data.get("last_traded_price")
        last_traded_on = call.data.get("last_traded_on")
        client_id = entry.options.get("client_id", entry.data.get("client_id"))
        client_secret = entry.options.get("client_secret", entry.data.get("client_secret"))
        
        token_info = await hass.async_add_executor_job(get_token, client_id, client_secret)
        access_token = token_info["access_token"]
        
        response = await hass.async_add_executor_job(send_custom_price, access_token, investment_id, last_traded_price, last_traded_on)
        
        if response.status_code == 200:
            _LOGGER.info(f"Price sent successfully to investment ID {investment_id}")
            # hass.components.persistent_notification.create(f"Price sent successfully to investment ID {investment_id}", title="Sharesight Success", notification_id=f"sharesight_success_{investment_id}")
        else:
            _LOGGER.error(f"Failed to send price to investment ID {investment_id}")
            # hass.components.persistent_notification.create(f"Failed to send price to investment ID {investment_id}", title="Sharesight Failure", notification_id=f"sharesight_failure_{investment_id}")

    hass.services.async_register(DOMAIN, "send_price", handle_send_price, schema=vol.Schema({
        vol.Required("investment_id"): cv.positive_int,
        vol.Required("last_traded_price"): cv.string,
        vol.Required("last_traded_on"): cv.string,
    }))

    return True

