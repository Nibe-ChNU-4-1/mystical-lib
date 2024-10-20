from flask import Blueprint, render_template, session, redirect, url_for

homepages_bp = Blueprint('homepages', __name__)

@homepages_bp.route('/admin')
def admin_home():
    if 'user' in session and session['user']['role'] == 'admin':
        return render_template('admin_home.html')
    return redirect(url_for('auth.login'))

@homepages_bp.route('/user')
def user_home():
    if 'user' in session and session['user']['role'] == 'user':
        return render_template('user_home.html')
    return redirect(url_for('auth.login'))


