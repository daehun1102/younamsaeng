from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import jwt
from datetime import datetime, timedelta
from pydantic_settings import BaseSettings

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class EmailConfig(BaseSettings):
    MAIL_USERNAME: str = "your_email@example.com"
    MAIL_PASSWORD: str = "your_password"
    MAIL_FROM: str = "your_email@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.example.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

# EmailConfig의 인스턴스 생성
email_config = EmailConfig()

# ConnectionConfig 생성
conf = ConnectionConfig(
    MAIL_USERNAME=email_config.MAIL_USERNAME,
    MAIL_PASSWORD=email_config.MAIL_PASSWORD,
    MAIL_FROM=email_config.MAIL_FROM,
    MAIL_PORT=email_config.MAIL_PORT,
    MAIL_SERVER=email_config.MAIL_SERVER,
    MAIL_STARTTLS=email_config.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_config.MAIL_SSL_TLS,
)

def create_verification_token(email: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_verification_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def send_verification_email(email: EmailStr, token: str):
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Click the link to verify your email: {verification_link}",
        subtype="html",
    )
    fm = FastMail(conf)
    fm.send_message(message)
