from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
import logging
from pokemon_controller import get_pokemon_by_name, list_all_pokemons, get_random_pokemon_by_type, get_longest_name_pokemon_by_type, save_pokemons_to_bd
from user_controller import get_user, login_user
from secure import encrypt_password, generate_token

app = Flask(__name__)

jwt = JWTManager(app)

@app.route('/pokemon/', methods=['GET'])
@jwt_required()
def get_all_pokemons():
    result = list_all_pokemons()
    return result

@app.route('/pokemon/name/<name>', methods=['GET'])
@jwt_required()
def get_pokemon(name):
    result = get_pokemon_by_name(name)
    return result

@app.route('/pokemon/type/<type>', methods=['GET'])
@jwt_required()
def get_random_pokemon_type(type):
    result = get_random_pokemon_by_type(type)
    return result

@app.route('/pokemon/longest-name/type/<type>', methods=['GET'])
@jwt_required()
def get_pokemon_type_longest_name(type):
    result = get_longest_name_pokemon_by_type(type)
    return result

@app.route('/pokemon/fill-bd', methods=['GET'])
@jwt_required()
def get_pokemon_from_pokeapi():
    result = save_pokemons_to_bd()
    return result

@app.route('/login', methods=['POST'])
def login():
    req = request.json
    username = req.get('username')
    password = req.get('password')

    if not username or not password:
        logging.error(f"Login error. Both user and pass are required")
        return jsonify({'error': 'Username and password are required'}), 400
    
    data = login_user(username)
    password_hash = encrypt_password(password)
    if data['password'] == password_hash:
        token = generate_token(username)
        response = make_response(jsonify({'message': 'Login successful'}), 201)
        response.headers['Authorization'] = 'Bearer ' + token
        logging.info(f"Login successful")
        return response
    logging.error(f"Login error. User or pass are not valid")
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/users/', methods=['GET'])
@jwt_required()
def show_user():
    result = get_user()
    return result


@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return jsonify({
        'error': 'Missing Authorization Header. Must include a valid token'
    }), 401

@jwt.invalid_token_loader
def custom_invalid_token_response(callback):
    return jsonify({
        'error': 'Invalid token'
    }), 401

@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token has expired'
    }), 401

def not_found(error):
    response = make_response(jsonify({'Error': 'Not found. Write a valid URI'}))
    response.status_code = 404
    return response