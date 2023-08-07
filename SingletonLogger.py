import settings
import logging

class SingletonLogger():    
    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls._instance = settings.logging.getLogger("bot")
        return cls._instance
