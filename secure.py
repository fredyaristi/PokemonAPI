import hashlib
import os
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from datetime import timedelta
from azure.identity import EnvironmentCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.secrets import SecretClient

secret = os.getenv('JWT_SECRET_KEY')

def generate_token(identity):
    expire = timedelta(hours=1)
    return create_access_token(identity=identity,expires_delta=expire)    

def encrypt_password(passwd):
    return hashlib.sha256(passwd.encode('utf-8')).hexdigest()

def get_secret(vault_url, secret_name):
    credential = EnvironmentCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value