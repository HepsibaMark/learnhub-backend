from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from config import Config
import mysql.connector

auth_bp = Blueprint('auth', __name__)

def get_db():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT
    )

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    role = data.get('role', 'student')
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)', (name, email, hashed, role))
        db.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        token = create_access_token(identity=str(user['id']))
        return jsonify({'token': token, 'role': user['role'], 'name': user['name']}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401
