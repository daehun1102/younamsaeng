from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import SessionLocal, User

app = FastAPI()

# DB Session 관리
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic 모델: 수정 데이터 구조 정의
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

# 사용자 수정 (Update)
@app.put("/admin/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 변경 가능한 필드 업데이트
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.password = user_update.password  # 실제로는 비밀번호 해시를 생성해야 함

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": {"id": user.id, "username": user.username, "email": user.email}}

# 사용자 삭제 (Delete)
@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"} 