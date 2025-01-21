from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''
declatrive_base()?
SQLAlchemy에서 ORM(Object Relational Mapping)을 설정하기 위해 사용. DB Table과 Python Class 간의 매핑을 정의. 
1. 기반 클래스 생성: 모든 모델 클래스는 이 기반 클래스를 상속받아 정의됨
2. 테이블 매핑 지원: __tablename__ 속성을 DB 테이블 이름과 연결 -> 클래스의 속성(Column)을 테이블의 열(column)과 매핑
3. 메타데이터 관리: schema에 대한 정보를 Base.metadata에 저장. -> 테이블 생성, 삭제 등 작업 가능
'''
Base = declarative_base() 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)

DATABASE_URL = "sqlite:///./test.db"

'''
create_engine()?
DB에 연결하기 위한 엔진을 생성 -> 이 엔진으로 DB와의 모든 상호작용이 이루어짐 -> 다양한 DB 지원, 설정 및 디버깅 옵션 제공
'''
engine = create_engine(DATABASE_URL)

'''
sessionmaker()?
sessionmaker로 sessionfactory(DB 연결과 트랜잭션 관리 일관성 있게 처리 가능하게 해줌) 생성 -> 작업(CRUD수행)을 수행할 때마다 SessionLocal로 세션 객체 생성 -> 작업이 끝난 후 close()로 세션 종료
'''
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)