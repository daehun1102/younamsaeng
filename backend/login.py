'''
A Basic user authentication system [User registration, Email verification, Login]
- Pydantic: Data validation
- SQLAlchemy: DB operations
- bcrypt: PW hashing

Enhancement
- Add expiration for verification tokens using tool like Redis
- Use an SMTP server or email API to send actual verification email
- Use JWT for session management and authentications
'''


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field, ValidationError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
from backend.database import SessionLocal, User

app = FastAPI()

# Pw hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 메모리 내 인증 토큰 저장(demo)
verification_tokens = {}  # 실제 서비스에는 Redis 같은 외부 캐시 저장소 사용

# 회원가입 시 Client가 보내는 데이터의 구조를 나타내는 Pydantic 모델


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    is_verified: bool

    class Config:
        from_attributes = True

# DB session 관리


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# pw hash function


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create user


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(username=user_data.username,
                   email=user_data.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# 1. 회원가입 endpoint
'''
DB에서 email 중복 여부 확인 -> 인증 토큰 생성, 사용자의 데이터를 메모리에 저장 -> 이메일 인증 링크 생성해 출력
'''


@app.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 인증 토큰 생성 및 저장
    token = secrets.token_urlsafe(16)
    verification_tokens[token] = user.model_dump()

    # 이메일 전송 시뮬레이션 (실제로는 이메일 전송 API 사용)
    print(
        f"Email verification link: http://localhost:8000/verify-email/{token}")
    return {"message": "Please verify your email to complete registration"}

# 2. email verification endpoint
'''
verification token을 이용해 메모리에서 사용자의 데이터 가져옴 -> 토큰이 없거나 만료되면 error 반환 -> db에 사용자를 저장하고 인증 완료 메세지 반환
'''


@app.get("/verify-email/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user_data = verification_tokens.pop(token, None)
    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # 사용자 생성
    user = create_user(db, UserCreate(**user_data))
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return {"message": "Email verified successfully. Registration complete", "user": UserInDB.model_validate(user)}

# 3. Login Endpoint


@app.post("/login/")
async def login_user(email: EmailStr, password: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=400, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    return {"message": "Login successful", "user": UserInDB.model_validate(user)}
