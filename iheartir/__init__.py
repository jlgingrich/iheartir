from pkg_resources import iter_entry_points
import logging
import logging.config

log_config = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s'
        },
        'simple': {
            'format': '%(levelname)s:%(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'WARNING',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'logs/iheartir.last.log'
        }
    },
    'root': {
        'handlers': ['console', 'logfile'],
        'level': 'DEBUG'
    }
}

logging.config.dictConfig(log_config)

logging.debug("Sucessfully started logger")

def get_providers():
    return {entry_point.load() for entry_point in iter_entry_points('iheartir.providers')}