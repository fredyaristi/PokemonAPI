from dotenv import load_dotenv
from flask import jsonify, make_response
import logging
import random
from database import get_db
from external import get_pokemons_from_pokeapi

load_dotenv()

#Método para listar todos los Pokemon
def list_all_pokemons():
    try:
        #Obtiene objeto de conexion de BD
        db = get_db()
        #Consulta todos los Pokemon
        results = list(db.pokemons.find({}, {'_id':0}).sort('id', 1))
        if results:
            #Construye respuesta de datos en json
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

#Método para consulta Pokemon segun su nombre
def get_pokemon_by_name(name):
    try:
        #Obtiene objeto de conexion de BD
        db = get_db()
        #Consulta Pokemon por nombre y almacena nombre, tipo y habilidad sin el ID
        result = db.pokemons.find_one({"name": name}, {"_id": 0, "name": 1, "types": 1, "ability": 1})
        if result:
            #Construye respuesta para retornarla
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

#Método para consulta de Pokemon aleatorio segun su tipo
def get_random_pokemon_by_type(type):
    try:
        types = [type]
        db = get_db()
        #Filtra los Pokemos por el tipo entregado y almacena nombre, tipo y habilidad.
        result = list(db.pokemons.find({"types": {"$all": types}}, {"_id": 0, "name": 1, "types": 1, "ability": 1}))
        if result:
            #Escoge un objeto aleatorio de los almacenados y construye la respuesta para retornarla
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

#Método para obtener el Pokemon con el nombre más largo según su tipo
def get_longest_name_pokemon_by_type(type):
    try:
        types = [type]
        db = get_db()
        #Consulta y filtra los Pokemon por su tipo y almacena nombre, tipo y habilitad.
        result = list(db.pokemons.find({"types": {"$all": types}}, {"_id": 0, "name": 1, "types": 1, "ability": 1}))
        if result:
            #Consulta el resultado y almacena el objeto con el campo name más grande
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

#Metodo para almacenar los Pokemon que se descargan desde la API pública
def save_pokemons_to_bd():
    #Almacena los Pokemon que se descargan desde la API
    pokemons = get_pokemons_from_pokeapi()
    if pokemons:
        try:
            db = get_db()
            #Almacena respuesta del insert a la BD de los Pokemon
            saved = db.pokemons.insert_many(pokemons)
            if saved:
                #Escribe registro indicando la cantidad de Pokemon almacenados en la BD
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