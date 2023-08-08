import settings
import logging 

'''
I'm aware this isn't a true singleton pattern, but it's close enough for my purposes atm, and I will likely edit it in the future
to be more of a true singleton pattern.
'''

logger = settings.logging.getLogger("bot")

def get_logger():
    return logger
    

    
