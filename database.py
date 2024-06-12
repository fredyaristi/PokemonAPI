from pymongo import MongoClient
import os
from dotenv import load_dotenv
from secure import get_secret
import logging

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_db():
    secret_name_db = os.getenv('SECRET_NAME_DB')
    vault_url = os.getenv('AZURE_VAULT_URL')
    database_url = get_secret(vault_url, secret_name_db)

    try:
        client = MongoClient(database_url)
        db = client.get_default_database()
        return db
    except Exception as e:
        logging.error(f"Connection to DB failed: {e}")
        return ({'Error': 'Connection to DB failed'})