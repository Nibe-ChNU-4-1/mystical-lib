from flask import Blueprint, request, jsonify, session, redirect, url_for
from database import relics_collection
from bson.objectid import ObjectId
import requests

relics_bp = Blueprint('relics', __name__)

# Створити нову реліквію
@relics_bp.route('/relics', methods=['POST'])
def create_relic():
    data = request.get_json()
    relic = {
        'name': data['name'],
        'description': data['description'],
        'available': data['available'],
        'owner': data['owner']
    }
    relics_collection.insert_one(relic)
    return jsonify({'message': 'Relic created successfully'}), 201

# Отримати всі реліквії
@relics_bp.route('/relics', methods=['GET'])
def get_relics():
    relics = list(relics_collection.find())
    for relic in relics:
        relic['_id'] = str(relic['_id'])
    return jsonify(relics), 200

# Отримати одну реліквію
@relics_bp.route('/relics/<relic_id>', methods=['GET'])
def get_relic(relic_id):
    relic = relics_collection.find_one({'_id': ObjectId(relic_id)})
    if relic:
        relic['_id'] = str(relic['_id'])
        return jsonify(relic), 200
    return jsonify({'error': 'Relic not found'}), 404

# Оновити реліквію
@relics_bp.route('/relics/<relic_id>', methods=['PUT'])
def update_relic(relic_id):
    data = request.get_json()
    updated_relic = {
        'name': data['name'],
        'description': data['description'],
        'available': data['available'],
        'owner': data['owner']
    }
    result = relics_collection.update_one({'_id': ObjectId(relic_id)}, {'$set': updated_relic})
    if result.modified_count > 0:
        return jsonify({'message': 'Relic updated successfully'}), 200
    return jsonify({'error': 'Relic not found'}), 404

# Видалити реліквію
@relics_bp.route('/relics/<relic_id>', methods=['DELETE'])
def delete_relic(relic_id):
    result = relics_collection.delete_one({'_id': ObjectId(relic_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Relic deleted successfully'}), 200
    return jsonify({'error': 'Relic not found'}), 404

# Взяти реліквію
@relics_bp.route('/relics/take/<relic_id>', methods=['POST'])
def take_relic(relic_id):
    if 'user' not in session:
        # Якщо користувач не авторизований, перенаправити його на сторінку логіну
        return redirect(url_for('auth.login'))

    # Знайти реліквію
    relic = relics_collection.find_one({'_id': ObjectId(relic_id)})
    if not relic:
        return jsonify({'error': 'Relic not found'}), 404

    # Оновити власника та змінити статус на недоступний
    relics_collection.update_one(
        {'_id': ObjectId(relic_id)},
        {'$set': {'available': False, 'owner': session['user']['username']}}
    )

    return redirect(url_for('homepages.catalog'))  # Повернутись на сторінку каталогу