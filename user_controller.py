from dotenv import load_dotenv
from flask import jsonify
import logging
from database import get_db

load_dotenv()

def get_user():
    try:
        db = get_db()
        results = list(db.users.find({}, {'_id':0}))
        if results:
            return  results
    except Exception as e:
        logging.error(f"Error fetching all users (get_user): {e}")
        return jsonify({'error': 'Error fetching users from DB'}), 500

def login_user(username):
    try:
        db = get_db()
        user = db.users.find_one({'username': username})
        if user:
            return user
    except Exception as e:
        logging.error(f"Error fetching user (login_user): {e}")
        return jsonify({'error': 'Error user login'}), 500

