from pymongo import MongoClient
import os
from dotenv import load_dotenv
from secure import get_secret
import logging

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Método para inicializar conexión con la BD
def get_db():
    #Nombre del secreto en Key Vault para la cadena de conexión
    secret_name_db = os.getenv('SECRET_NAME_DB')
    #URL del Key Vault
    vault_url = os.getenv('AZURE_VAULT_URL')
    #Obtener cadena de conexión desde el Key Vault
    database_url = get_secret(vault_url, secret_name_db)

    try:
        #Conexion a BD usando librería pymongo
        client = MongoClient(database_url)
        #Obtener BD por defecto
        db = client.get_default_database()
        #Retornar la conexión a la BD para ser usada en las consultas
        return db
    except Exception as e:
        #Registrar errores en archivo de logs
        logging.error(f"Connection to DB failed: {e}")
        return ({'Error': 'Connection to DB failed'})