import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here_make_it_long_123456')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://learnhub_db_e2z3_user:NERDEgbokMitHbZyWYqMywClIweNhXWn@dpg-d8q4uvgg4nts7381vu80-a.oregon-postgres.render.com/learnhub_db_e2z3')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key_here_make_it_long_123456')
