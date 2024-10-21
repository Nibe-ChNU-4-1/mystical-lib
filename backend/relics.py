from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from database import relics_collection
from bson.objectid import ObjectId
import requests

relics_bp = Blueprint('relics', __name__)

# Створити нову реліквію
@relics_bp.route('/relics/create', methods=['POST'])
def create_relic():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('auth.login'))

    data = request.form
    new_relic = {
        'name': data['name'],
        'description': data['description'],
        'available': True,  # За замовчуванням доступна
        'owner': 'archive'  # За замовчуванням власник — архів
    }

    relics_collection.insert_one(new_relic)
    flash('New relic successfully created!')
    return redirect(url_for('homepages.admin_home'))

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
@relics_bp.route('/relics/update/<relic_id>', methods=['POST'])
def update_relic(relic_id):
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('auth.login'))

    relic = relics_collection.find_one({"_id": ObjectId(relic_id)})
    if relic:
        updated_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'available': 'available' in request.form  # Оновлення доступності
        }
        relics_collection.update_one({"_id": ObjectId(relic_id)}, {"$set": updated_data})
        flash("Relic updated successfully!")
        return redirect(url_for('homepages.admin_home'))
    else:
        flash("Relic not found!")
        return redirect(url_for('homepages.admin_home'))


# Видалити реліквію
@relics_bp.route('/relics/<relic_id>/delete', methods=['POST'])
def delete_relic(relic_id):
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('auth.login'))

    result = relics_collection.delete_one({'_id': ObjectId(relic_id)})

    if result.deleted_count > 0:
        flash('Relic successfully deleted.')
    else:
        flash('Error: Relic not found or could not be deleted.')

    return redirect(url_for('homepages.admin_home'))

# Взяти реліквію
@relics_bp.route('/relics/take/<relic_id>', methods=['POST'])
def take_relic(relic_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    relic = relics_collection.find_one({'_id': ObjectId(relic_id)})
    if not relic:
        return jsonify({'error': 'Relic not found'}), 404

    relics_collection.update_one(
        {'_id': ObjectId(relic_id)},
        {'$set': {'available': False, 'owner': session['user']['username']}}
    )

    return redirect(url_for('homepages.catalog'))


@relics_bp.route('/relics/<relic_id>/return', methods=['POST'])
def return_relic(relic_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))

    relic = relics_collection.find_one({'_id': ObjectId(relic_id), 'owner': user['username']})

    if relic:
        relics_collection.update_one(
            {'_id': ObjectId(relic_id)},
            {'$set': {'available': True, 'owner': "Archive"}}
        )
        return redirect(url_for('homepages.user_home'))
    return jsonify({'error': 'Relic not found or not owned by user'}), 404