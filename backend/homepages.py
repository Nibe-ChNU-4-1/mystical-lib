from flask import Blueprint, render_template

homepages_bp = Blueprint('homepages', __name__)

@homepages_bp.route('/admin')
def admin_home():
    return render_template('admin_home.html')

@homepages_bp.route('/user')
def user_home():
    return render_template('user_home.html')
