from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from config import Config

users_bp = Blueprint('users', __name__)

def get_db():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

@users_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll():
    user_id = get_jwt_identity()
    data = request.get_json()
    course_id = data['course_id']
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)', (user_id, course_id))
        db.commit()
        return jsonify({'message': 'Enrolled successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        db.close()

@users_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT c.* FROM courses c JOIN enrollments e ON c.id = e.course_id WHERE e.user_id = %s', (user_id,))
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(courses), 200
