from flask import Blueprint, render_template, session, redirect, url_for
from relics import *
import requests

homepages_bp = Blueprint('homepages', __name__)

@homepages_bp.route('/admin')
def admin_home():
    if 'user' in session and session['user']['role'] == 'admin':
        return render_template('admin_home.html')
    return redirect(url_for('auth.login'))

@homepages_bp.route('/user')
def user_home():
    if 'user' in session and session['user']['role'] == 'user':
        user_relics = relics_collection.find({'owner': session['user']['username']})
        user_relics = list(user_relics)
        return render_template('user_home.html', user_relics=user_relics)
    return redirect(url_for('auth.login'))

@homepages_bp.route('/catalog')
def catalog():
    response = requests.get('http://localhost:5000/relics')
    relics = response.json()
    return render_template('catalog.html', relics=relics)

@homepages_bp.route('/take_relic/<relic_id>', methods=['POST'])
def take_relic(relic_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session['username']
    relic = get_relic_by_id(relic_id)

    if relic['available']:
        update_relic_owner(relic_id, username)
        flash('You have successfully taken the relic.')
    else:
        flash('This relic is already taken by someone else.')

    return redirect(url_for('catalog'))

