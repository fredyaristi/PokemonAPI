import logging

class Config:
    DEBUG = True

config = {
    'dev': Config
}

# Configuración del logging
logging.basicConfig(filename='./logs/logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')