from homeassistant_api import Client
from config.aiotconfig import config

client = Client(config["api_url"], config["api_key"], cache_session=False)
