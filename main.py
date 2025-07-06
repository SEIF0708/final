import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from user import db
from auth import auth_bp

app = Flask(__name__, static_folder='static')

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app, origins="*")
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Create tables
with app.app_context():
    db.create_all()

# Serve frontend files (index, login, signup)
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/login.html')
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route('/signup.html')
def serve_signup():
    return send_from_directory('.', 'signup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 