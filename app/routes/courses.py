from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from config import Config

courses_bp = Blueprint('courses', __name__)

def get_db():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM courses WHERE is_published = TRUE')
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(courses), 200

@courses_bp.route('/courses', methods=['POST'])
@jwt_required()
def add_course():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data['title']
    description = data.get('description', '')
    price = data.get('price', 0.00)
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO courses (instructor_id, title, description, price, is_published) VALUES (%s, %s, %s, %s, %s)', (user_id, title, description, price, True))
        db.commit()
        return jsonify({'message': 'Course created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        db.close()

@courses_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    cursor.execute('SELECT * FROM modules WHERE course_id = %s', (course_id,))
    modules = cursor.fetchall()
    for module in modules:
        cursor.execute('SELECT * FROM lessons WHERE module_id = %s', (module['id'],))
        module['lessons'] = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'course': course, 'modules': modules}), 200
