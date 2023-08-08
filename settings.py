import os
import logging
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
twitter_api_key = os.getenv("twitter_api_key")
twitter_api_secret = os.getenv("twitter_secret_api_key")
twitter_access_token = os.getenv("twitter_access_token")
twitter_access_token_secret = os.getenv("twitter_secret_access_token")
weather_api_key = os.getenv("weather_api_key")
lastfm_api_key = os.getenv("lastfm_api_key")
lastfm_secret_api_key = os.getenv("lastfm_secret")
db_name = os.getenv("db_name")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose":{
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard":{
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console":{
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2":{
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file":{
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w",
            'formatter': "verbose"
        },
    },
    "loggers": {
        "bot":{
            "handlers": ['console'],
            "level": "INFO",
            "propogate": False
        },
        "discord":{
            "handlers": ['console2', "file"],
            "level": "INFO",
            "propogate": False
        },
        "discord.ext.commands":{
            "handlers": ['console2'],
            "level": "WARNING",
            "propogate": False
        }
    }

}

dictConfig(LOGGING_CONFIG)