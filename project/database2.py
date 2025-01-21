from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
from passlib.context import CryptContext

# Database URL
DATABASE_URL = "sqlite:///./test.db"  # 원하는 데이터베이스 URL로 변경 가능

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base 클래스 정의
Base = declarative_base()

# 세션 로컬 정의
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)

# 데이터베이스 테이블 생성
def initialize_database():
    Base.metadata.create_all(bind=engine)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_verified INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

# 사용자 생성
def create_user(email: str, password: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_password = pwd_context.hash(password)
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("User with this email already exists.")
    finally:
        conn.close()

# 사용자 인증
def verify_user_credentials(email: str, password: str) -> bool:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_password = row[0]
        return pwd_context.verify(password, stored_password)
    return False

# 사용자 활성화 (이메일 인증)
def activate_user(email: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_verified = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

# 데이터베이스 초기화 호출
init_db()