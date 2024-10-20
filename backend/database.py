from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
users_collection = db['users']
relics_collection = db['relics']

def init_db():
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
    if 'relics' not in db.list_collection_names():
        db.create_collection('relics')

def add_user(username, password, role):
    user_data = {
        'username': username,
        'password': password,
        'role': role
    }
    users_collection.insert_one(user_data)

def get_user(username):
    return users_collection.find_one({'username': username})
