from flask import Blueprint, jsonify, send_file, request
from flask_jwt_extended import decode_token
import mysql.connector
from config import Config
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
import os

certificate_bp = Blueprint('certificate', __name__)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'certificates'))

def get_db():
    return mysql.connector.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DB)

@certificate_bp.route('/certificate/<int:course_id>', methods=['GET'])
def get_certificate(course_id):
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token missing'}), 401
    decoded = decode_token(token)
    user_id = decoded['sub']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT u.name, c.title FROM users u JOIN enrollments e ON u.id = e.user_id JOIN courses c ON c.id = e.course_id WHERE u.id = %s AND c.id = %s', (user_id, course_id))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    if not data:
        return jsonify({'error': 'Not enrolled'}), 400
    os.makedirs(BASE_DIR, exist_ok=True)
    filename = 'certificate_' + str(user_id) + '_' + str(course_id) + '.pdf'
    filepath = os.path.join(BASE_DIR, filename)
    w, h = landscape(A4)
    c = canvas.Canvas(filepath, pagesize=landscape(A4))
    c.setFillColor(colors.HexColor('#0056D2'))
    c.rect(0, 0, w, h, fill=1)
    c.setFillColor(colors.white)
    c.rect(30, 30, w-60, h-60, fill=1)
    c.setFillColor(colors.HexColor('#0056D2'))
    c.rect(30, 30, w-60, 8, fill=1)
    c.rect(30, h-38, w-60, 8, fill=1)
    c.setFillColor(colors.HexColor('#0056D2'))
    c.setFont('Helvetica-Bold', 48)
    c.drawCentredString(w/2, h-120, 'LearnHub')
    c.setFillColor(colors.HexColor('#333333'))
    c.setFont('Helvetica', 20)
    c.drawCentredString(w/2, h-160, 'CERTIFICATE OF COMPLETION')
    c.setStrokeColor(colors.HexColor('#0056D2'))
    c.setLineWidth(1)
    c.line(w/2-150, h-175, w/2+150, h-175)
    c.setFillColor(colors.HexColor('#555555'))
    c.setFont('Helvetica', 16)
    c.drawCentredString(w/2, h-220, 'This is to certify that')
    c.setFillColor(colors.HexColor('#0056D2'))
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(w/2, h-270, data['name'])
    c.setStrokeColor(colors.HexColor('#0056D2'))
    c.line(w/2-180, h-285, w/2+180, h-285)
    c.setFillColor(colors.HexColor('#555555'))
    c.setFont('Helvetica', 16)
    c.drawCentredString(w/2, h-320, 'has successfully completed the course')
    c.setFillColor(colors.HexColor('#333333'))
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(w/2, h-370, data['title'])
    c.setFillColor(colors.HexColor('#888888'))
    c.setFont('Helvetica', 12)
    c.drawCentredString(w/2, h-430, 'Issued by LearnHub | www.learnhub.com')
    c.save()
    return send_file(filepath, as_attachment=True)
