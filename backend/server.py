from flask import Flask, render_template, session
from auth import auth_bp
from homepages import homepages_bp
from database import init_db
from pymongo import MongoClient
from relics import relics_bp

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
app.config['SECRET_KEY'] = 'your_secret_key'

app.register_blueprint(auth_bp)
app.register_blueprint(homepages_bp)
app.register_blueprint(relics_bp)

init_db()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





