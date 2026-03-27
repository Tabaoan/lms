import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

def generate_id(): return str(uuid.uuid4())

@router.post("/parents")
def create_parent(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    db_parent = models.Parent(id=generate_id(), **parent.model_dump())
    db.add(db_parent)
    db.commit()
    return db_parent

@router.get("/parents/{parent_id}")
def get_parent(parent_id: str, db: Session = Depends(get_db)):
    return db.query(models.Parent).filter(models.Parent.id == parent_id).first()

@router.post("/students")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(id=generate_id(), **student.model_dump())
    db.add(db_student)
    db.commit()
    return db_student

@router.post("/subscriptions")
def create_subscription(sub: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    db_sub = models.Subscription(id=generate_id(), **sub.model_dump())
    db.add(db_sub)
    db.commit()
    return db_sub