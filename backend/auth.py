from flask import Blueprint, request, redirect, render_template, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_user, add_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'username': user['username'],
                'role': user['role']
            }
            if user['role'] == 'admin':
                return redirect(url_for('homepages.admin_home'))
            else:
                return redirect(url_for('homepages.user_home'))
        return "Invalid credentials"
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')
        add_user(username, generate_password_hash(password), role)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
