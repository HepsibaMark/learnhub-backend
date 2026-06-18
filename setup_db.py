import psycopg2
from config import Config

conn = psycopg2.connect(Config.DATABASE_URL)
cursor = conn.cursor()

commands = [
    """CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'student',
        profile_pic VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS courses (
        id SERIAL PRIMARY KEY,
        instructor_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        thumbnail VARCHAR(255),
        price DECIMAL(8,2) DEFAULT 0.00,
        is_published BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS modules (
        id SERIAL PRIMARY KEY,
        course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        title VARCHAR(200) NOT NULL,
        order_num INT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS lessons (
        id SERIAL PRIMARY KEY,
        module_id INT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
        title VARCHAR(200) NOT NULL,
        content_url VARCHAR(500),
        type VARCHAR(10) DEFAULT 'video',
        duration_sec INT DEFAULT 0,
        order_num INT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS enrollments (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, course_id)
    )""",
    """CREATE TABLE IF NOT EXISTS progress (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        lesson_id INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
        completed BOOLEAN DEFAULT FALSE,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, lesson_id)
    )""",
    """CREATE TABLE IF NOT EXISTS quizzes (
        id SERIAL PRIMARY KEY,
        module_id INT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
        title VARCHAR(200) NOT NULL,
        pass_score INT DEFAULT 50
    )""",
    """CREATE TABLE IF NOT EXISTS quiz_questions (
        id SERIAL PRIMARY KEY,
        quiz_id INT NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
        question TEXT NOT NULL,
        options JSONB NOT NULL,
        correct_index INT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS quiz_attempts (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        quiz_id INT NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
        score INT NOT NULL,
        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS certificates (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        cert_url VARCHAR(500),
        issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, course_id)
    )"""
]

for command in commands:
    cursor.execute(command)

conn.commit()
cursor.close()
conn.close()
print("All tables created successfully!")