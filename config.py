import logging

#Habilitación del modo debug en la aplicación
class Config:
    DEBUG = True

config = {
    'dev': Config
}

# Configuración del logging para almacenar en la ruta /logs
logging.basicConfig(filename='./logs/logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')