import requests
import logging
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Metodo para descargar los Pokemon desde la API publica
def get_pokemons_from_pokeapi():
    offset = 0
    #Cant de Pokemon que se quieren descargar
    limit = os.getenv('POKEMONS_AMOUNT')
    pokemons = []

    while True:
        #Construye la url completa para consultar los pokemon
        url = f"{os.getenv('PUBLIC_POKEAPI_URL')}/?limit={limit}&offset={offset}"
        
        try:
            #Descarga y almacena los nombres de los Pokemon
            response = requests.get(url)
        
            if response.status_code != 200:
                break
            #Da formato a los datos para manipularlos
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                break
            #Descarga los tipos y habilidades de cada Pokemon segun su nombre
            for result in results:
                pokemon_name = result['name']
                pokemon_data = requests.get(f"{os.getenv('PUBLIC_POKEAPI_URL')}/{pokemon_name}").json()
                pokemon_type = [tipo['type']['name'] for tipo in pokemon_data['types']]
                pokemon_abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
                #Construye los datos de cada Pokemon
                pokemon = {
                    'id': pokemon_data['id'],
                    'name': pokemon_data['name'],
                    'types': pokemon_type,
                    'ability': pokemon_abilities
                }
                #Almacena los datos de cada Pokemon a la lista
                pokemons.append(pokemon)
            
            offset += 100
            logging.info(f"'{len(pokemons)}' were download from PokeApi")
            return pokemons
        except Exception as e:
            logging.error(f"Error downloading Pokemons from PokeAPI: '{e}'")
            return "Error downloading Pokemons from PokeAPI"