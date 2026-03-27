import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ĐỔI SANG SQLITE ĐỂ CỨU BÀI TEST NGAY LẬP TỨC
DATABASE_URL = "sqlite:///./lms_test.db"

# Thêm connect_args này để FastAPI chạy mượt với SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()