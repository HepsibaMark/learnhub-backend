from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    JWTManager(app)
    from app.routes.auth import auth_bp
    from app.routes.courses import courses_bp
    from app.routes.users import users_bp
    from app.routes.certificate import certificate_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(courses_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')
    return app
