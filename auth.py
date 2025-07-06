from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from user import db, User
from werkzeug.security import generate_password_hash
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    full_name = data.get('fullName', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if len(full_name) < 2:
        return jsonify({'error': 'Full name must be at least 2 characters long'}), 400
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({'error': 'Invalid email address'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    if User.find_by_email(email):
        return jsonify({'error': 'Email address is already registered'}), 409
    user = User(full_name=full_name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({
        'message': 'User registered successfully',
        'user': {'id': user.id, 'full_name': user.full_name, 'email': user.email},
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    user = User.find_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({
        'message': 'Login successful',
        'user': {'id': user.id, 'full_name': user.full_name, 'email': user.email},
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200 