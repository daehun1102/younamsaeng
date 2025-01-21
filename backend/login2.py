from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from emailAuth2 import send_verification_email
from database2 import create_user, verify_user_credentials

app = FastAPI()

class RegisterModel(BaseModel):
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

@app.post("/register")
async def register(user: RegisterModel):
    # 사용자 등록
    create_user(user.email, user.password)
    # 인증 이메일 발송
    send_verification_email(user.email)
    return {"message": "A verification email has been sent. Please check your inbox."}

@app.post("/userlogin")
async def user_login(credentials: LoginModel):
    # 사용자 인증 확인
    if verify_user_credentials(credentials.email, credentials.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
