from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
from config import Config

courses_bp = Blueprint('courses', __name__)

def get_db():
    return psycopg2.connect(Config.DATABASE_URL)

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, instructor_id, title, description, price, is_published, created_at FROM courses WHERE is_published = TRUE')
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    courses = [{'id': r[0], 'instructor_id': r[1], 'title': r[2], 'description': r[3], 'price': str(r[4]), 'is_published': r[5], 'created_at': str(r[6])} for r in rows]
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
    cursor = db.cursor()
    cursor.execute('SELECT id, instructor_id, title, description, price FROM courses WHERE id = %s', (course_id,))
    r = cursor.fetchone()
    course = {'id': r[0], 'instructor_id': r[1], 'title': r[2], 'description': r[3], 'price': str(r[4])} if r else None
    cursor.execute('SELECT id, title, order_num FROM modules WHERE course_id = %s', (course_id,))
    module_rows = cursor.fetchall()
    modules = []
    for m in module_rows:
        cursor.execute('SELECT id, title FROM lessons WHERE module_id = %s', (m[0],))
        lessons = [{'id': l[0], 'title': l[1]} for l in cursor.fetchall()]
        modules.append({'id': m[0], 'title': m[1], 'lessons': lessons})
    cursor.close()
    db.close()
    return jsonify({'course': course, 'modules': modules}), 200
