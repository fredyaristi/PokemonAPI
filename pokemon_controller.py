from dotenv import load_dotenv
from flask import jsonify, make_response
import logging
import random
from database import get_db
from external import get_pokemons_from_pokeapi

load_dotenv()

def list_all_pokemons():
    try:
        db = get_db()
        results = list(db.pokemons.find({}, {'_id':0}).sort('id', 1))
        if results:
            response = make_response(jsonify(results))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify({'message': 'Error fetching pokemons from DB'}))
            response.status_code = 404
            return response
    except Exception as e:
        logging.error(f"Error fetching all pokemons (list_all_pokemons): {e}")
        response = make_response(jsonify({'message': 'Error fetching pokemons from DB'}))
        response.status_code = 404
        return response

def get_pokemon_by_name(name):
    try:
        #Find in DB
        db = get_db()
        result = db.pokemons.find_one({"name": name}, {"_id": 0, "name": 1, "types": 1, "ability": 1})
        if result:
            response = make_response(jsonify(result))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify({'message': 'Error. Pokemon not found'}))
            response.status_code = 404
            return response
    except Exception as e:
        logging.error(f"Error Pokemon not found: {e}")
        response = make_response(jsonify({'message': 'Error. Pokemon not found'}))
        response.status_code = 404
        return response

def get_random_pokemon_by_type(type):
    try:
        types = [type]
        db = get_db()
        result = list(db.pokemons.find({"types": {"$all": types}}, {"_id": 0, "name": 1, "types": 1, "ability": 1}))
        if result:
            result = random.choice(result)
            response = make_response(jsonify(result))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify({"message": f"Type '{type}' not found"}))
            response.status_code = 404
            return response
    except Exception as e:
        logging.error(f"Error consultando pokemon por tipo: {e}")
        response = make_response(jsonify({"message": f"Type '{type}' not found"}))
        response.status_code = 404
        return response

def get_longest_name_pokemon_by_type(type):
    try:
        types = [type]
        db = get_db()
        result = list(db.pokemons.find({"types": {"$all": types}}, {"_id": 0, "name": 1, "types": 1, "ability": 1}))
        if result:
            longest_name_pokemon = max(result, key=lambda x: len(x['name']))
            response = make_response(jsonify(longest_name_pokemon))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify({"message": f"Type '{type}' not found"}))
            response.status_code = 404
            return response
    except Exception as e:
        logging.error(f"Error consultando pokemon por tipo: {e}")
        response = make_response(jsonify({"message": f"Type '{type}' not found"}))
        response.status_code = 404
        return response

def save_pokemons_to_bd():
    pokemons = get_pokemons_from_pokeapi()
    if pokemons:
        try:
            db = get_db()
            saved = db.pokemons.insert_many(pokemons)
            if saved:
                logging.info(f"'{len(pokemons)}' Pokemon saved in the BD from PokeApi")
                response = make_response(jsonify({'message': f'{len(pokemons)} pokemon saved in the BD from public PokeApi'}))
                response.status_code = 200
                return response
            else:
                response = make_response(jsonify({"message": f"Error saving Pokemon in the BD"}))
                response.status_code = 404
                logging.info(f"'{len(pokemons)}' Pokemon saved in the BD from PokeApi")
                return response
        except Exception as e:
            logging.error(f"Error': 'Pokemons not saved in the BD: {e}")
            response = make_response(jsonify({"message": f"Pokemons not saved"}))
            response.status_code = 404
            return response
    else:
        logging.error(f"Error consultando pokemon: {e}")
        response = make_response(jsonify({"message": f"Error fetching pokemon from PokeApi"}))
        response.status_code = 404
        return response