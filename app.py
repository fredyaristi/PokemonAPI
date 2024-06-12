import os
from config import config
from routes import app, not_found
from secure import get_secret

secret_name_jwt = os.getenv('SECRET_NAME_JWT')
vault_url = os.getenv('AZURE_VAULT_URL')
jwt_token = get_secret(vault_url, secret_name_jwt)

if __name__ == "__main__":
    app.config.from_object(config['dev'])
    app.register_error_handler(404, not_found)
    app.config["JWT_SECRET_KEY"] = jwt_token
    app.run(host="0.0.0.0", port=5000)